from pathlib import Path

import asyncio
import inspect
import logging
import os
import random
import types

from pyee import AsyncIOEventEmitter

import aiohttp
import websockets


try:
    from orjson import loads
    from orjson import dumps as _dumps
    dumps = lambda d: _dumps(d).decode("utf-8")
except ModuleNotFoundError:
    try:
        from ujson import loads
        from ujson import dumps
    except ModuleNotFoundError:
        from json import loads
        from json import dumps


logging.basicConfig(format="[%(name)s:%(funcName)s:%(lineno)s] %(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)


DL_ROOT = "https://raw.githubusercontent.com/ChromeDevTools/devtools-protocol/master/json"
SOURCE_FILES = [
    f"{DL_ROOT}/browser_protocol.json",
    f"{DL_ROOT}/js_protocol.json"
]

MAX_INT = (2 ** 31) - 1


def get_cache_folder():
    cache_dir = os.environ.get("CDIPY_CACHE")
    if cache_dir:
        return cache_dir

    xdg_cache_home = os.getenv("XDG_CACHE_HOME")
    if not xdg_cache_home:
        user_home = os.getenv("HOME")
        if user_home:
            xdg_cache_home = os.path.join(user_home, ".cache")

    if xdg_cache_home:
        return os.path.join(xdg_cache_home, "python-cdipy")

    return os.path.join(os.path.dirname(__file__), ".cache")


async def download_data():
    async with aiohttp.ClientSession() as session:
        requests = []
        for url in SOURCE_FILES:
            logger.debug("Downloading %s", url)
            requests.append(session.get(url))

        responses = await asyncio.gather(*requests)
        for response in responses:
            new_path = CACHE_FOLDER / response.url.name
            with open(new_path, "w+b") as f:
                f.write(await response.read())
            logger.debug("Wrote %s", new_path)


CACHE_FOLDER = Path(get_cache_folder())
if not os.path.exists(CACHE_FOLDER):
    os.makedirs(CACHE_FOLDER, mode=0o744)

if not os.listdir(CACHE_FOLDER):
    asyncio.get_event_loop().run_until_complete(download_data())


def get_domains():
    domains = []
    for filename in os.listdir(CACHE_FOLDER):
        with open(CACHE_FOLDER / filename, "rb") as f:
            data = loads(f.read())
        domains += data.get("domains", [])
    return domains

DOMAINS = get_domains()


def create_signature(params):
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
            default=default)

        new_params.append(new_param)

    new_params.sort(key=lambda p: bool(p.default), reverse=True)

    return inspect.Signature(parameters=new_params)


class DomainProxy:
    """
        Template class used for domains (ex: obj.Page)
    """

    def __init__(self, devtools):
        self.devtools = devtools


def wrap_factory(command_name, signature):
    """
        Creates a new function that can be used as a domain method
    """

    async def wrapper(self, *args, **kwargs):
        """
            - Validate method arguments against <signature>
            - Attempt to execute method
        """
        bound = signature.bind(*args, **kwargs)
        kwargs = bound.arguments
        command = f"{self.__class__.__name__}.{command_name}"
        return await self.devtools.execute_method(command, **kwargs)

    return wrapper


class ResponseErrorException(Exception):
    pass


class UnknownMessageException(Exception):
    pass


class Devtools(AsyncIOEventEmitter):

    def __init__(self):
        super().__init__()

        self.future_map = {}
        self.command_id = random.randint(0, 2**16)

        self.populate_domains()
        self.loop = asyncio.get_event_loop()


    def wait_for(self, event, timeout=0):
        """
            Wait for a specific event to fire before returning
        """
        future = asyncio.get_event_loop().create_future()

        def update_future(*args, **kwargs):
            future.set_result((args, kwargs))

        self.once(event, update_future)
        if timeout:
            return asyncio.wait_for(future, timeout)

        return future


    def populate_domains(self):
        """
            Generate domain classes (ex: self.Page) and methods (ex: self.Page.enable)
        """
        for domain in DOMAINS:
            # Create a new class for each domain with the correct name
            domain_class = types.new_class(domain["domain"], (DomainProxy, ))
            new_instance = domain_class(self)
            for command in domain.get("commands", []):
                # Create a new method for each domain command
                method_sig = create_signature(command.get("parameters", []))
                new_fn = wrap_factory(command["name"], method_sig)
                new_method = types.MethodType(new_fn, new_instance)
                setattr(new_instance, command["name"], new_method)

            setattr(self, domain["domain"], new_instance)


    def format_command(self, method, **kwargs):
        """
            Convert method name + arguments to a devtools command
        """
        self.command_id += 1

        return {
            "id": self.command_id,
            "method": method,
            "params": kwargs
        }


    async def handle_message(self, message):
        """
            Match incoming message ids against our dict of pending futures
            Emit events for incomming methods
        """
        message = loads(message)

        if "id" in message:
            if message["id"] not in self.future_map:
                return

            future = self.future_map.pop(message["id"])
            if not future.done():
                if "error" in message:
                    future.set_exception(ResponseErrorException(message["error"]["message"]))
                else:
                    future.set_result(message["result"])

        elif "method" in message:
            self.emit(message["method"], **message["params"])

        else:
            raise UnknownMessageException(f"Unknown message format: {message}")


    async def execute_method(self, method, **kwargs):
        """
            Called by the wrap_factory wrapper with the method name and validated arguments
        """
        command = self.format_command(method, **kwargs)

        result_future = self.loop.create_future()
        self.future_map[command["id"]] = result_future

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


    async def connect(self):
        self.websocket = await websockets.connect(
            self.ws_uri,
            max_queue=None,
            max_size=None,
            read_limit=MAX_INT,
            write_limit=MAX_INT,
            ping_interval=None)
        self.task = asyncio.ensure_future(self._recv_loop())


    def __del__(self):
        if hasattr(self, 'task'):
            self.task.cancel()


    async def _recv_loop(self):
        while True:
            try:
                recv_data = await self.websocket.recv()
                logger.debug("recv: %s", recv_data)

            except websockets.exceptions.ConnectionClosed:
                logger.error("Websocket connection closed")
                break

            await self.handle_message(recv_data)


    async def send(self, command):
        logger.debug("send: %s", command)
        await self.websocket.send(dumps(command))


class ChromeDevToolsTarget(Devtools):

    def __init__(self, devtools, session):
        super().__init__()

        self.devtools = devtools
        self.devtools.on("Target.receivedMessageFromTarget", self._target_recv)

        self.session = session


    async def _target_recv(self, sessionId, message, **_):
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
        self.future_map[command["id"]] = result_future

        await self.devtools.Target.sendMessageToTarget(dumps(command), self.session)

        return await result_future
