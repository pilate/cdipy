import asyncio
import logging
import typing
from itertools import count

import msgspec
import websockets.asyncio.client
import websockets.asyncio.connection
import websockets.exceptions
from pyee.asyncio import AsyncIOEventEmitter

from .exceptions import ResponseErrorException, UnknownMessageException
from .protocol import DOMAINS


LOGGER = logging.getLogger("cdipy.cdipy")


class MessageError(msgspec.Struct):  # pylint: disable=too-few-public-methods
    message: str


class Message(msgspec.Struct):  # pylint: disable=too-few-public-methods
    id: int = None
    method: str = None
    params: typing.Any = None
    result: typing.Any = None
    error: MessageError = None


MSG_DECODER = msgspec.json.Decoder(type=Message)
MSG_ENCODER = msgspec.json.Encoder()


class DevtoolsEmitter(AsyncIOEventEmitter):
    def __init__(self):
        super().__init__()

        self.loop = asyncio.get_event_loop()

    def wait_for(self, event: str, timeout: int = 0) -> asyncio.Future:
        """
        Wait for a specific event to fire before returning
        """
        future = self.loop.create_future()

        def update_future(*args, **kwargs):
            future.set_result((args, kwargs))

        self.once(event, update_future)
        if timeout:
            return asyncio.wait_for(future, timeout)

        return future


class Devtools(DevtoolsEmitter):
    def __init__(self):
        super().__init__()

        self.futures = {}
        self.counter = count()

    def __getattr__(self, attr: str):
        """
        Load each domain on demand
        """
        if domain := DOMAINS.get(attr):
            setattr(self, attr, domain(self))

        return super().__getattribute__(attr)

    def format_command(self, method: str, **kwargs) -> dict:
        """
        Convert method name + arguments to a devtools command
        """
        return {"id": next(self.counter), "method": method, "params": kwargs}

    async def handle_message(self, message: str) -> None:
        """
        Match incoming message ids to self.futures
        Emit events for incoming methods
        """
        message = MSG_DECODER.decode(message)

        if message.id is not None:
            future = self.futures.pop(message.id)
            if not future.cancelled():
                if error := message.error:
                    future.set_exception(ResponseErrorException(error.message))
                else:
                    future.set_result(message.result)

        elif message.method:
            self.emit(message.method, **message.params)

        elif message.error:
            raise ResponseErrorException(message.error.message)

        else:
            raise UnknownMessageException(f"Unknown message format: {message}")

    async def execute_method(self, method: str, **kwargs) -> dict:
        """
        Called by the add_command wrapper with the method name and validated arguments
        """
        command = self.format_command(method, **kwargs)

        result_future = self.loop.create_future()
        self.futures[command["id"]] = result_future

        await self.send(command)

        return await result_future

    async def send(self, command):
        raise NotImplementedError


class ChromeDevTools(Devtools):
    def __init__(self, websocket_uri: str):
        super().__init__()

        self.task: asyncio.Future | None = None
        self.ws_uri: str | None = websocket_uri
        self.websocket: websockets.asyncio.connection.Connection = None

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
        self.task = asyncio.ensure_future(self._recv_loop())

    async def _recv_loop(self):
        while True:
            try:
                recv_data = await self.websocket.recv(decode=None)
                LOGGER.debug("recv: %s", recv_data)

            except websockets.exceptions.ConnectionClosed:
                LOGGER.error("Websocket connection closed")
                break

            await self.handle_message(recv_data)

    async def send(self, command: dict) -> None:
        LOGGER.debug("send: %s", command)
        await self.websocket.send(MSG_ENCODER.encode(command), text=True)


class ChromeDevToolsTarget(Devtools):  # pylint: disable=abstract-method
    def __init__(self, devtools: ChromeDevTools, session: str):
        super().__init__()

        self.devtools = devtools
        self.devtools.on("Target.receivedMessageFromTarget", self._target_recv)

        self.session = session

    async def _target_recv(
        self, sessionId, message, **_
    ):  # pylint: disable=invalid-name
        if sessionId != self.session:
            return
        
        await self.handle_message(message)

    async def execute_method(self, method: str, **kwargs):
        """
        Target commands are in the same format, but sent as a parameter to
        the sendMessageToTarget method
        """
        command = self.format_command(method, **kwargs)

        result_future = self.loop.create_future()
        self.futures[command["id"]] = result_future

        message = MSG_ENCODER.encode(command).decode()
        await self.devtools.Target.sendMessageToTarget(message, self.session)

        return await result_future
