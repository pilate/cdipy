import asyncio
import json
import logging
import typing
from itertools import count

import msgspec
import websockets.asyncio.client
import websockets.asyncio.connection
import websockets.exceptions

from .exceptions import ResponseErrorException, UnknownMessageException
from .protocol import DOMAINS


LOGGER = logging.getLogger("cdipy.cdipy")


class EventEmitter:
    """Minimal event emitter replacing pyee.AsyncIOEventEmitter."""

    def __init__(self):
        self._listeners = {}
        self._once_listeners = {}

    def on(self, event, listener):
        if not asyncio.iscoroutinefunction(listener):
            raise TypeError(f"{listener!r} must be a coroutine function")
        self._listeners.setdefault(event, []).append(listener)

    def once(self, event, listener):
        if not asyncio.iscoroutinefunction(listener):
            raise TypeError(f"{listener!r} must be a coroutine function")
        self._once_listeners.setdefault(event, []).append(listener)

    def off(self, event, listener):
        for mapping in (self._listeners, self._once_listeners):
            if entries := mapping.get(event):
                entries.remove(listener)
                if not entries:
                    del mapping[event]

    def emit(self, event, *args, **kwargs):
        listeners = self._listeners.get(event, ())
        once = self._once_listeners.pop(event, ())
        for listener in listeners:
            self.loop.create_task(listener(*args, **kwargs))
        for listener in once:
            self.loop.create_task(listener(*args, **kwargs))


class MessageError(msgspec.Struct):  # pylint: disable=too-few-public-methods
    message: str


class Message(msgspec.Struct):  # pylint: disable=too-few-public-methods
    id: int = None
    method: str = None
    params: typing.Any = None
    result: typing.Any = None
    error: MessageError = None
    sessionId: str = None


class Command(msgspec.Struct, omit_defaults=True):  # pylint: disable=too-few-public-methods
    id: int
    method: str
    params: dict
    sessionId: str = None


MSG_DECODER = msgspec.json.Decoder(type=Message)
MSG_ENCODER = msgspec.json.Encoder()


class Devtools(EventEmitter):
    def __init__(self):
        super().__init__()

        self.loop = asyncio.get_running_loop()
        self.futures = {}
        self.counter = count()

    def wait_for(self, event: str, timeout: int = 0) -> asyncio.Future:
        """
        Wait for a specific event to fire before returning
        """
        future = self.loop.create_future()

        async def update_future(*args, **kwargs):
            future.set_result((args, kwargs))

        self.once(event, update_future)
        if timeout:
            return asyncio.wait_for(future, timeout)

        return future

    def __getattr__(self, attr: str):
        """
        Load each domain on demand
        """
        if domain := DOMAINS.get(attr):
            setattr(self, attr, domain(self))

        return super().__getattribute__(attr)

    def _process_message(self, message_obj: Message) -> None:
        """
        Match incoming message ids to self.futures
        Emit events for incoming methods
        """
        if message_obj.id is not None:
            future = self.futures.pop(message_obj.id)
            if not future.cancelled():
                if error := message_obj.error:
                    future.set_exception(ResponseErrorException(error.message))
                else:
                    future.set_result(message_obj.result)

        elif message_obj.method:
            self.emit(message_obj.method, **(message_obj.params or {}))

        elif message_obj.error:
            raise ResponseErrorException(message_obj.error.message)

        else:
            raise UnknownMessageException(f"Unknown message format: {message_obj}")

    async def execute_method(self, method: str, **kwargs) -> dict:
        """
        Called by the add_command wrapper with the method name and validated arguments
        """
        cmd_id = next(self.counter)
        future = self.loop.create_future()
        self.futures[cmd_id] = future

        await self.send(Command(id=cmd_id, method=method, params=kwargs))

        return await future

    async def send(self, command: Command):
        raise NotImplementedError


class ChromeDevTools(Devtools):
    def __init__(self, websocket_uri: str):
        super().__init__()

        self.task: asyncio.Future | None = None
        self.ws_uri: str | None = websocket_uri
        self.websocket: websockets.asyncio.connection.Connection = None
        self.sessions: dict[str, ChromeDevToolsTarget] = {}

    def __del__(self):
        if task := getattr(self, "task", None):
            task.cancel()

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
        while True:
            try:
                recv_data = await self.websocket.recv(decode=None)
            except websockets.exceptions.ConnectionClosed:
                LOGGER.error("Websocket connection closed")
                break

            try:
                message_obj = MSG_DECODER.decode(recv_data)
            except msgspec.DecodeError:
                message_obj = Message(**json.loads(recv_data))

            if target := self.sessions.get(message_obj.sessionId):
                target._process_message(message_obj)
            else:
                self._process_message(message_obj)

    async def send(self, command: Command) -> None:
        await self.websocket.send(MSG_ENCODER.encode(command), text=True)


class ChromeDevToolsTarget(Devtools):
    def __init__(self, devtools: ChromeDevTools, session: str):
        super().__init__()

        self.devtools = devtools
        self.devtools.sessions[session] = self
        self.session = session

    async def send(self, command: Command) -> None:
        command.sessionId = self.session
        await self.devtools.send(command)
