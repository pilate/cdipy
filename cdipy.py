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

import websockets



logger = logging.getLogger("cdipy.chrome")
logging.basicConfig(format="[%(asctime)s] [%(levelname)s] %(message)s", level=logging.DEBUG)

logging.getLogger("websockets").setLevel(logging.ERROR)


DEFAULT_ARGS = [
    "--disable-background-networking",
    "--disable-background-timer-throttling",
    "--disable-breakpad",
    "--disable-client-side-phishing-detection",
    "--disable-default-apps",
    "--disable-extensions",
    "--disable-hang-monitor",
    "--disable-popup-blocking",
    "--disable-prompt-on-repost",
    "--disable-sync",
    "--disable-translate",
    "--enable-automation",
    "--metrics-recording-only",
    "--no-first-run",
    "--password-store=basic",
    "--remote-debugging-port=0",
    "--safebrowsing-disable-auto-update",
    "--use-mock-keychain",
    "--headless",
    "--disable-gpu",
    "--hide-scrollbars",
    "--mute-audio"
]

CHROME_PATH = "/usr/bin/google-chrome-stable"
WS_RE = re.compile(r"listening on (ws://[^ ]*)")


class ChromeRunner(object):

    def __init__(self, proxy=None):
        super().__init__()

        self.proxy = proxy

        self.tmp_path = Path(tempfile.mkdtemp())
        self.websocket_uri = None


    # Browser cleanup
    def __del__(self):
         # Kill chrome and all of its child processes
        try:
            os.killpg(os.getpgid(self.proc_pid), signal.SIGKILL)
        except:
            logger.debug("Failed to kill chrome processes")

        # Empty the user data directory
        try:
            shutil.rmtree(self.tmp_path)
        except:
            logger.debug(f"Failed to delete user-data-dir: {self.tmp_path}")


    async def launch(self, chrome_path=CHROME_PATH):
        command = [chrome_path] + DEFAULT_ARGS + [f"--user-data-dir={self.tmp_path}"]
        if self.proxy:
            command += [f"--proxy-server={self.proxy}"]

        self.proc = await asyncio.create_subprocess_exec(*command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, preexec_fn=os.setsid)
        self.proc_pid = self.proc.pid

        output = ""
        while True:
            if self.proc.returncode is not None:
                stderr = await self.proc.stdout.read()
                raise Exception(f"Chrome closed unexpectedly with return code: {self.proc.returncode} ({stderr})")

            data = await self.proc.stdout.readline()
            output += data.decode()

            search = WS_RE.search(output)
            if search:
                break

        self.websocket_uri = search.group(1).strip()
        logger.info(f"Parsed websocket URI: {self.websocket_uri}")


def create_signature(params):
    """
        Creates a function signature based on protocol parameters
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

    def __init__(self, devtools):
        self.devtools = devtools


def wrap_factory(command_name, signature):
    """
        Returns a function that will validate its arguments against <signature>
         and attempt to execute the command
    """

    async def wrapper(self, *args, **kwargs):
        bound = signature.bind(*args, **kwargs)
        kwargs = bound.arguments
        command = f"{self.__class__.__name__}.{command_name}"
        return await self.devtools.execute_method(command, **kwargs)
    return wrapper


def populate_domains(obj, domains):
    """
        Add domains and methods to obj (ex: obj.Page, obj.Network)

        DomainProxy is the template for all domains
        wrap_factory is used to generate the methods
    """

    for domain in domains:
        # Create a new class for each domain with the correct name
        domain_class = types.new_class(domain["domain"], (DomainProxy, ))
        new_instance = domain_class(obj)
        for command in domain.get("commands", []):
            method_sig = create_signature(command.get("parameters", []))
            new_fn = wrap_factory(command["name"], method_sig)
            new_method = types.MethodType(new_fn, new_instance)
            setattr(new_instance, command["name"], new_method)

        setattr(obj, domain["domain"], new_instance)


class Devtools(EventEmitter):

    def __init__(self):
        super().__init__()

        self.future_map = {}
        self.command_id = random.randint(0, 2**16)

        self.loop = asyncio.get_event_loop()


    def format_command(self, method, **kwargs):
        self.command_id += 1

        return {
            "id": self.command_id,
            "method": method,
            "params": kwargs
        }


    async def handle_message(self, message):
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


    async def _target_recv(self, sessionId, message, targetId=None):
        await self.handle_message(message)


class ChromeDevTools(Devtools):

    def __init__(self, websocket_uri, protocol):
        super().__init__()

        self.ws_uri = websocket_uri
        self.protocol = protocol

        populate_domains(self, self.protocol["domains"])

        self.on("Target.receivedMessageFromTarget", self._target_recv)


    async def connect(self):
        self.websocket = await websockets.client.connect(self.ws_uri, 
            max_size=2**40, read_limit=2**40, max_queue=0)
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


    async def execute_method(self, method, **kwargs):
        command = self.format_command(method, **kwargs)

        result_future = self.loop.create_future()
        self.future_map[command["id"]] = result_future

        await self.send(command)

        return await result_future


class ChromeDevToolsTarget(Devtools):

    def __init__(self, devtools, session):
        super().__init__()

        self.devtools = devtools
        self.devtools.on("Target.receivedMessageFromTarget", self._target_recv)

        self.session = session

        populate_domains(self, self.devtools.protocol["domains"])


    async def execute_method(self, method, **kwargs):
        command = self.format_command(method, **kwargs)

        result_future = self.loop.create_future()
        self.future_map[command["id"]] = result_future

        await self.devtools.Target.sendMessageToTarget(json.dumps(command), self.session)

        return await result_future