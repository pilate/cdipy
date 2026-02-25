import asyncio
import json
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
    sessionId: str = None


MSG_DECODER = msgspec.json.Decoder(type=Message)
MSG_ENCODER = msgspec.json.Encoder()


class Devtools(AsyncIOEventEmitter):
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

        def update_future(*args, **kwargs):
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
            self.emit(message_obj.method, **message_obj.params)

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

        await self.send({"id": cmd_id, "method": method, "params": kwargs})

        return await future

    async def send(self, command):
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
                LOGGER.debug("recv: %s", recv_data)

            except websockets.exceptions.ConnectionClosed:
                LOGGER.error("Websocket connection closed")
                break

            try:
                message_obj = MSG_DECODER.decode(recv_data)
            except msgspec.DecodeError:
                message_obj = Message(**json.loads(recv_data))

            if message_obj.sessionId in self.sessions:
                self.sessions[message_obj.sessionId]._process_message(message_obj)
            else:
                self._process_message(message_obj)

    async def send(self, command: dict) -> None:
        LOGGER.debug("send: %s", command)
        await self.websocket.send(MSG_ENCODER.encode(command), text=True)


class ChromeDevToolsTarget(Devtools):
    def __init__(self, devtools: ChromeDevTools, session: str):
        super().__init__()

        self.devtools = devtools
        self.devtools.sessions[session] = self
        self.session = session

    async def send(self, command: dict) -> None:
        command["sessionId"] = self.session
        await self.devtools.send(command)
