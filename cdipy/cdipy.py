from pathlib import Path

import asyncio
import asyncio.subprocess as subprocess
import inspect
import logging
import os
import random
import re
import shutil
import signal
import tempfile
import types

from pyee import EventEmitter

try:
    import ujson as json
except:
    import json

import aiohttp
import websockets



logging.basicConfig(format="[%(name)s:%(funcName)s:%(lineno)s] %(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)


SOURCE_FILES = [
    "https://raw.githubusercontent.com/ChromeDevTools/devtools-protocol/master/json/browser_protocol.json",
    "https://raw.githubusercontent.com/ChromeDevTools/devtools-protocol/master/json/js_protocol.json"
]

CACHE_FOLDER_DEFAULT = os.path.join(os.path.dirname(__file__), '.cache/')
CACHE_FOLDER = Path(os.path.expanduser(os.environ.get("PROTOCOL_CACHE", CACHE_FOLDER_DEFAULT)))


async def download_data():
    async with aiohttp.ClientSession() as session:
        requests = []
        for url in SOURCE_FILES:
            logger.debug(f"Downloading {url}")
            requests.append(session.get(url))

        responses = await asyncio.gather(*requests)
        for response in responses:
            new_path = CACHE_FOLDER / response.url.name
            open(new_path, "w+b").write(await response.read())
            logger.debug(f"Wrote {new_path}")
            
if not os.path.exists(CACHE_FOLDER):
    os.mkdir(CACHE_FOLDER, mode=0o744)

if not os.listdir(CACHE_FOLDER):
    asyncio.get_event_loop().run_until_complete(download_data())

DOMAINS = []
for filename in os.listdir(CACHE_FOLDER):
    data = json.load(open(CACHE_FOLDER / filename, "rb"))
    DOMAINS += data.get("domains", [])


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

    return inspect.Signature(parameters=new_params)


class DomainProxy(object):
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


class Devtools(EventEmitter):

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
        else:
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
        message = json.loads(message)

        if "id" in message:
            if message["id"] not in self.future_map:
                return

            future = self.future_map.pop(message["id"])
            if "error" in message:
                future.set_exception(Exception(message["error"]["message"]))
            else:
                future.set_result(message["result"])

        elif "method" in message:
            self.emit(message["method"], **message["params"])

        else:
            raise Exception(f"Unknown message format: {message}")


    async def execute_method(self, method, **kwargs):
        """
            Called by the wrap_factory wrapper with the method name and validated arguments
        """
        command = self.format_command(method, **kwargs)

        result_future = self.loop.create_future()
        self.future_map[command["id"]] = result_future

        await self.send(command)

        return await result_future


class ChromeDevTools(Devtools):

    def __init__(self, websocket_uri):
        super().__init__()

        self.ws_uri = websocket_uri


    async def connect(self):
        self.websocket = await websockets.client.connect(self.ws_uri, 
            max_size=2**32, read_limit=2**32, max_queue=2**32)
        self.task = asyncio.ensure_future(self._recv_loop())


    async def _recv_loop(self):
        while True:
            try:
                recv_data = await self.websocket.recv()
                logger.debug(f"recv: {recv_data}")

            except websockets.exceptions.ConnectionClosed:
                logger.error("Websocket connection closed")
                break

            await self.handle_message(recv_data)


    async def send(self, command):
        logger.debug(f"send: {command}")
        await self.websocket.send(json.dumps(command))


class ChromeDevToolsTarget(Devtools):

    def __init__(self, devtools, session):
        super().__init__()

        self.devtools = devtools
        self.devtools.on("Target.receivedMessageFromTarget", self._target_recv)

        self.session = session


    async def _target_recv(self, sessionId, message, targetId=None):
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

        await self.devtools.Target.sendMessageToTarget(json.dumps(command), self.session)

        return await result_future
