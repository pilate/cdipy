import asyncio
import inspect
import logging
import os
import sys
import types
from itertools import count

import websockets
import websockets.client
from pyee import AsyncIOEventEmitter

from cdipy.utils import get_cache_path, update_protocol_data
from cdipy.fjson import dumps, loads


LOGGER = logging.getLogger("cdipy.cdipy")

DOMAINS = {}


class DomainBase:  # pylint: disable=too-few-public-methods
    """
    Template class used for domains (ex: obj.Page)
    """

    __slots__ = ("devtools",)

    def __init__(self, devtools):
        self.devtools = devtools


def params_to_signature(params):
    """
    Creates a function signature based on a list of protocol parameters
    """
    new_params = []

    for param in params:
        default = inspect.Parameter.empty
        if param.get("optional"):
            default = None

        new_param = inspect.Parameter(
            name=param["name"],
            kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
            default=default,
        )

        new_params.append(new_param)

    new_params.sort(key=lambda p: bool(p.default), reverse=True)

    return inspect.Signature(parameters=new_params)


def add_command(domain_class, command):
    """
    Creates a new function that can be used as a domain method
    """
    command_name = command["name"]
    command_str = f"{domain_class.__name__}.{command_name}"

    signature = params_to_signature(command.get("parameters", []))

    async def wrapper(self, *args, **kwargs):
        """
        Validate method arguments against `signature`
        Pass validated args to execute_method
        """
        bound = signature.bind(*args, **kwargs)
        kwargs = bound.arguments
        return await self.devtools.execute_method(command_str, **kwargs)

    wrapper.__name__ = wrapper.__qualname__ = command_str

    setattr(domain_class, command_name, wrapper)


def load_domains():
    cache_path = get_cache_path()

    if not os.path.exists(cache_path):
        os.makedirs(cache_path, mode=0o744)

    if not os.listdir(cache_path):
        asyncio.get_event_loop().run_until_complete(update_protocol_data())

    domains = {}
    for filename in os.listdir(cache_path):
        with open(cache_path / filename, "rb") as f:  # pylint: disable=invalid-name
            data = loads(f.read())

        for domain in data.get("domains", []):
            domain_name = domain["domain"]

            # Create a new class for each domain
            domain_class = types.new_class(domain_name, (DomainBase,))

            # Add each command to the domain class
            for command in domain.get("commands", []):
                add_command(domain_class, command)

            domains[domain_name] = domain_class

    return domains


DOMAINS = load_domains()


class ResponseErrorException(Exception):
    pass


class UnknownMessageException(Exception):
    pass


class DevtoolsEmitter(AsyncIOEventEmitter):
    def __init__(self):
        super().__init__()

        self.loop = asyncio.get_event_loop()

    def wait_for(self, event, timeout=0):
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

    def __getattr__(self, attr):
        """
        Load each domain on demand
        """
        if domain := DOMAINS.get(attr):
            setattr(self, attr, domain(self))

        return super().__getattribute__(attr)

    def format_command(self, method, **kwargs):
        """
        Convert method name + arguments to a devtools command
        """

        return {"id": next(self.counter), "method": method, "params": kwargs}

    async def handle_message(self, message):
        """
        Match incoming message ids to self.futures
        Emit events for incoming methods
        """
        message = loads(message)

        if "id" in message:
            future = self.futures.pop(message["id"])
            if not future.cancelled():
                if error := message.get("error"):
                    future.set_exception(ResponseErrorException(error["message"]))
                else:
                    future.set_result(message["result"])

        elif "method" in message:
            self.emit(message["method"], **message["params"])

        else:
            raise UnknownMessageException(f"Unknown message format: {message}")

    async def execute_method(self, method, **kwargs):
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
    def __init__(self, websocket_uri):
        super().__init__()

        self.task = None
        self.websocket = None
        self.ws_uri = websocket_uri

    def __del__(self):
        if task := getattr(self, "task", None):
            task.cancel()

    async def connect(self, compression=None):
        self.websocket = await websockets.client.connect(
            self.ws_uri,
            max_queue=None,
            max_size=None,
            read_limit=2**24,
            write_limit=2**24,
            ping_interval=None,
            compression=compression,
        )
        self.task = asyncio.ensure_future(self._recv_loop())

    async def _recv_loop(self):
        while True:
            try:
                recv_data = await self.websocket.recv()
                LOGGER.debug("recv: %s", recv_data)

            except websockets.exceptions.ConnectionClosed:
                LOGGER.error("Websocket connection closed")
                break

            await self.handle_message(recv_data)

    async def send(self, command):
        LOGGER.debug("send: %s", command)
        await self.websocket.send(dumps(command))


class ChromeDevToolsTarget(Devtools):  # pylint: disable=abstract-method
    def __init__(self, devtools, session):
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

    async def execute_method(self, method, **kwargs):
        """
        Target commands are in the same format, but sent as a parameter to
        the sendMessageToTarget method
        """
        command = self.format_command(method, **kwargs)

        result_future = self.loop.create_future()
        self.futures[command["id"]] = result_future

        await self.devtools.Target.sendMessageToTarget(dumps(command), self.session)

        return await result_future
