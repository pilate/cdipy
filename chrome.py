from pathlib import Path

import asyncio
import asyncio.subprocess as subprocess
import logging
import os
import random
import re
import shutil
import signal
import tempfile

from pyee import EventEmitter

import ujson
import websockets

from domains.Browser import Browser
from domains.Network import Network
from domains.Page import Page
from domains.Target import Target



logger = logging.getLogger('cdt')
logging.basicConfig(format="[%(asctime)s] [%(levelname)s] %(message)s", level=logging.DEBUG)


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


# Browser process
class ChromeDevTools(EventEmitter):

    def __init__(self, proxy=None):
        super().__init__()

        self.proxy = proxy

        self.command_id = 0
        self.tmp_path = Path(tempfile.mkdtemp())
        self.connected = False
        self.loop = asyncio.get_event_loop()
        self.future_map = {}
        self.attached_session = None


    # Browser cleanup
    async def close(self):
         # Kill chrome and all of its child processes
        try:
            os.killpg(os.getpgid(self.proc_pid), signal.SIGKILL)
        except:
            logger.debug("Failed to kill browser processes")

        # Empty the user data directory
        try:
            shutil.rmtree(self.tmp_path)
        except:
            logger.debug("Failed to delete temp folder")


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

        self.ws_uri = search.group(1).strip()
        logger.info(f"Found websocket URI: {self.ws_uri}")

        self.websocket = await websockets.client.connect(self.ws_uri, 
            max_size=2**40, read_limit=2**40, max_queue=0)
        self.task = asyncio.ensure_future(self._recv_loop())

        self.on("Target.attachedToTarget", self._attached)
        self.on("Target.receivedMessageFromTarget", self._target_recv)

        self.connected = True
        self.Browser = Browser(self)
        self.Network = Network(self)
        self.Target = Target(self)
        self.Page = Page(self)


    async def send(self, command):
        if not self.connected:
            raise websockets.ConnectionClosed()

        logger.debug(f"send: {command}")
        await self.websocket.send(ujson.dumps(command))


    async def handle_message(self, message):
        if "id" in message:
            if "error" in message:
                self.future_map[message["id"]].set_exception(
                    Exception(message["error"]["message"]))
            else:
                self.future_map[message["id"]].set_result(message["result"])

            del self.future_map[message["id"]]
        
        elif "method" in message:
            self.emit(message["method"], **message["params"])

        else:
            raise Exception(f"Unknown message format: {message}")


    async def _recv_loop(self):
        while True:
            try:
                recv_data = await self.websocket.recv()
                logger.debug(f"recv: {recv_data}")

            except websockets.exceptions.ConnectionClosed:
                logger.error("Websocket connection closed")
                break

            except Exception as e:
                logger.warn(f"failed to wait forever {e}")

            message = ujson.loads(recv_data)
            await self.handle_message(message)


    async def _attached(self, sessionId, targetInfo, waitingForDebugger):
        self.attached_session = sessionId


    async def _target_recv(self, sessionId, message, targetId=None):
        await self.handle_message(ujson.loads(message))


    def create_command(self, method, **kwargs):
        self.command_id += 1

        return {
            "id": self.command_id,
            "method": method,
            "params": kwargs
        }


    async def run_command(self, method, **kwargs):
        command = self.create_command(method, **kwargs)

        result_future = self.loop.create_future()
        self.future_map[command["id"]] = result_future

        await self.send(command)

        response = await result_future
        return response


    async def run_target_command(self, method, sessionId, **kwargs):
        command = self.create_command(method, **kwargs)

        result_future = self.loop.create_future()
        self.future_map[command["id"]] = result_future

        await self.Target.sendMessageToTarget(ujson.dumps(command), sessionId)

        response = await result_future
        return response




"""

connect(uri, *, create_protocol=None, timeout=10, max_size=2 ** 20, max_queue=2 ** 5, read_limit=2 ** 16, write_limit=2 ** 16, loop=None, origin=None, extensions=None, subprotocols=None, extra_headers=None, compression='deflate', **kwds)
connect(uri, *, create_protocol=None,             max_size=2 ** 20, max_queue=2 ** 5, read_limit=2 ** 16, write_limit=2 ** 16, loop=None, origin=None, extensions=None, subprotocols=None, extra_headers=None, compression='deflate', **kwds)

ping_interval=20, ping_timeout=20, close_timeout=10, 

"""