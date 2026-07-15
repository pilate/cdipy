import asyncio
import inspect
import json
import logging
import typing
from itertools import count

import msgspec
import websockets.asyncio.client
import websockets.asyncio.connection
import websockets.exceptions

from .exceptions import ChromeClosedException, ResponseErrorException
from .protocol import DOMAINS


LOGGER = logging.getLogger("cdipy.cdipy")


class EventEmitter:
    """
    Minimal event emitter replacing pyee.AsyncIOEventEmitter.

    Listeners may be plain callables or coroutine functions; plain callables
    run inline during emit(), coroutine functions are scheduled as tasks.
    """

    def __init__(self):
        self.loop = asyncio.get_running_loop()
        self._listeners = {}
        self._once_listeners = {}
        self._tasks = set()

    @staticmethod
    def _add(mapping, event, listener):
        if not callable(listener):
            raise TypeError(f"{listener!r} must be callable")
        entry = (listener, inspect.iscoroutinefunction(listener))
        mapping.setdefault(event, []).append(entry)

    def on(self, event, listener):
        self._add(self._listeners, event, listener)

    def once(self, event, listener):
        self._add(self._once_listeners, event, listener)

    def has_listeners(self, event) -> bool:
        return event in self._listeners or event in self._once_listeners

    def off(self, event, listener):
        for mapping in (self._listeners, self._once_listeners):
            if entries := mapping.get(event):
                entries[:] = [entry for entry in entries if entry[0] != listener]
                if not entries:
                    del mapping[event]

    def _task_done(self, task):
        self._tasks.discard(task)
        if not task.cancelled() and (exc := task.exception()):
            LOGGER.debug("Unhandled exception in event handler: %s", exc)

    def _schedule(self, coro):
        task = self.loop.create_task(coro)
        self._tasks.add(task)
        task.add_done_callback(self._task_done)

    def emit(self, event, **kwargs):
        listeners = self._listeners.get(event)
        once = self._once_listeners.pop(event, None)

        # snapshot the live list so listeners can call on/off mid-emit;
        # once entries were popped above, so they are already ours
        if listeners:
            entries = (*listeners, *once) if once else tuple(listeners)
        elif once:
            entries = once
        else:
            return

        for listener, is_async in entries:
            if is_async:
                self._schedule(listener(**kwargs))
                continue

            try:
                result = listener(**kwargs)
            except Exception:  # pylint: disable=broad-except
                LOGGER.exception("Error in %s handler %r", event, listener)
                continue

            # async callables that iscoroutinefunction can't detect
            # (e.g. an object with an async __call__)
            if result is not None and inspect.isawaitable(result):
                self._schedule(result)

    async def wait_for_complete(self):
        """Wait for all pending handler tasks to finish."""
        if self._tasks:
            await asyncio.gather(*self._tasks, return_exceptions=True)


class MessageError(msgspec.Struct):  # pylint: disable=too-few-public-methods
    message: str


class Message(msgspec.Struct):  # pylint: disable=too-few-public-methods
    id: int = None
    method: str = None
    params: typing.Any = None
    result: typing.Any = None
    error: MessageError = None
    sessionId: str = None


class Command(
    msgspec.Struct, omit_defaults=True
):  # pylint: disable=too-few-public-methods
    id: int
    method: str
    params: dict
    sessionId: str = None


MSG_DECODER = msgspec.json.Decoder(type=Message)
MSG_ENCODER = msgspec.json.Encoder()


class Devtools(EventEmitter):
    closed = False

    def __init__(self):
        super().__init__()

        self.futures = {}
        self.counter = count()
        self.session = None
        self.waiters = set()

    def wait_for(self, event: str, timeout: float = 0) -> asyncio.Future:
        """
        Wait for a specific event to fire before returning
        """
        if self.closed:
            raise ChromeClosedException("Websocket connection closed")

        future = self.loop.create_future()

        def update_future(**kwargs):
            if not future.done():
                future.set_result(kwargs)

        self.once(event, update_future)
        self.waiters.add(future)

        # Unregister the listener when the future is cancelled (ex: timeout)
        # or fails because the connection closed; a no-op when the event
        # fired normally
        def cleanup(_):
            self.waiters.discard(future)
            self.off(event, update_future)

        future.add_done_callback(cleanup)

        if timeout:
            return asyncio.wait_for(future, timeout)

        return future

    def fail_pending(self, exc: Exception) -> None:
        """
        Fail all in-flight command futures and event waiters
        """
        # snapshot: failing a waiter runs its done callback,
        # which mutates the set we are iterating
        pending = (*self.futures.values(), *self.waiters)
        self.futures.clear()

        for future in pending:
            if not future.done():
                future.set_exception(exc)

    def __getattr__(self, attr: str):
        """
        Load each domain on demand
        """
        if domain := DOMAINS.get(attr):
            setattr(self, attr, domain(self))

        return super().__getattribute__(attr)

    def process_message(self, message_obj: Message) -> None:
        """
        Match incoming message ids to self.futures
        Emit events for incoming methods
        """
        if method := message_obj.method:
            # skip the **params repack when nothing is subscribed
            if self.has_listeners(method):
                if message_obj.params:
                    self.emit(method, **message_obj.params)
                else:
                    self.emit(method)

        elif message_obj.id is not None:
            future = self.futures.pop(message_obj.id, None)
            if future is None:
                return

            if not future.cancelled():
                if error := message_obj.error:
                    future.set_exception(ResponseErrorException(error.message))
                else:
                    future.set_result(message_obj.result)

        elif message_obj.error:
            LOGGER.error("Protocol error: %s", message_obj.error.message)

        else:
            LOGGER.error("Unknown message format: %s", message_obj)

    async def execute_method(
        self, method: str, params: dict, wait: bool = True
    ) -> dict:
        """
        Called by the add_command wrapper with the method name and validated arguments
        """
        cmd_id = next(self.counter)

        if wait:
            future = self.futures[cmd_id] = self.loop.create_future()

        command = Command(
            id=cmd_id, method=method, params=params, sessionId=self.session
        )

        try:
            await self.send(command)

        except BaseException:
            self.futures.pop(cmd_id, None)
            raise

        if wait:
            return await future

        return None

    async def send(self, command: Command):
        raise NotImplementedError


class ChromeDevTools(Devtools):
    def __init__(self, websocket_uri: str):
        super().__init__()

        self.task: asyncio.Future | None = None
        self.ws_uri: str | None = websocket_uri
        self.websocket: websockets.asyncio.connection.Connection = None
        self.sessions: dict[str, ChromeDevToolsTarget] = {}
        self.closed = False

    def __del__(self):
        if task := getattr(self, "task", None):
            task.cancel()

    def evict_session(self, session_id: str) -> None:
        """
        Stop tracking a session and fail anything pending on it
        """
        if target := self.sessions.pop(session_id, None):
            target.detached = True
            target.fail_pending(ChromeClosedException("Session detached"))

    async def connect(self, compression: str | None = None) -> None:
        self.websocket = await websockets.asyncio.client.connect(
            self.ws_uri,
            compression=compression,
            max_size=None,
            max_queue=None,
            write_limit=0,
            ping_interval=None,
        )
        self.task = asyncio.create_task(self._recv_loop())

    async def _recv_loop(self):
        try:
            while True:
                try:
                    recv_data = await self.websocket.recv(decode=None)
                except websockets.exceptions.ConnectionClosed:
                    if not self.closed:
                        LOGGER.error("Websocket connection closed")
                    break

                try:
                    message_obj = MSG_DECODER.decode(recv_data)
                except msgspec.DecodeError:
                    # msgspec rejects escaped lone surrogates (chrome sends them in
                    # postData), but the stdlib json parser accepts them
                    try:
                        message_obj = msgspec.convert(json.loads(recv_data), Message)
                    except (
                        json.JSONDecodeError,
                        UnicodeDecodeError,
                        msgspec.ValidationError,
                    ):
                        LOGGER.exception("Failed to decode message: %.512s", recv_data)
                        continue

                try:
                    if not (session_id := message_obj.sessionId):
                        self.process_message(message_obj)
                    elif target := self.sessions.get(session_id):
                        target.process_message(message_obj)
                    else:
                        # don't let messages for detached/unknown sessions
                        # resolve browser-scope futures with matching ids
                        LOGGER.debug("Message for unknown session: %.512s", recv_data)

                    # detach events can arrive on any scope; evicting here
                    # covers them all
                    if message_obj.method == "Target.detachedFromTarget":
                        self.evict_session((message_obj.params or {}).get("sessionId"))
                except Exception:  # pylint: disable=broad-except
                    LOGGER.exception("Error processing message: %.512s", recv_data)

        finally:
            self.closed = True

            exc = ChromeClosedException("Websocket connection closed")

            for devtools in (self, *self.sessions.values()):
                devtools.fail_pending(exc)

            self.sessions.clear()

    async def close(self):
        self.closed = True
        if self.websocket:
            self.websocket.transport.close()
        if self.task and not self.task.done():
            await self.task

    async def send(self, command: Command) -> None:
        if self.closed:
            raise ChromeClosedException("Websocket connection closed")

        try:
            await self.websocket.send(MSG_ENCODER.encode(command), text=True)
        except websockets.exceptions.ConnectionClosed:
            self.closed = True
            raise ChromeClosedException("Websocket connection closed")


class ChromeDevToolsTarget(Devtools):
    def __init__(self, devtools: ChromeDevTools, session: str):
        super().__init__()

        self.devtools = devtools
        self.devtools.sessions[session] = self
        self.session = session
        self.detached = False

    @property
    def closed(self) -> bool:
        return self.detached or self.devtools.closed

    async def detach(self) -> None:
        """
        Detach from the target and stop tracking this session
        """
        try:
            await self.devtools.Target.detachFromTarget(sessionId=self.session)
        finally:
            self.devtools.evict_session(self.session)

    async def send(self, command: Command) -> None:
        # chrome responses for detached sessions are dropped by the recv
        # loop, so a command sent now would never resolve
        if self.detached:
            raise ChromeClosedException("Session detached")

        await self.devtools.send(command)
