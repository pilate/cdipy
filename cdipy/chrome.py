import asyncio
import logging
import os
import re
import shutil
import signal
import tempfile
from asyncio import subprocess
from pathlib import Path


LOGGER = logging.getLogger("cdipy.chrome")

CHROME_PATH = os.environ.get("CDIPY_CHROME_PATH", "/usr/bin/google-chrome-stable")
CHROME_PARAMS = [
    "--disable-background-networking",
    "--enable-features=NetworkService,NetworkServiceInProcess",
    "--disable-background-timer-throttling",
    "--disable-backgrounding-occluded-windows",
    "--disable-breakpad",
    "--disable-client-side-phishing-detection",
    "--disable-component-extensions-with-background-pages",
    "--disable-default-apps",
    "--disable-extensions",
    "--disable-features=Translate",
    "--disable-hang-monitor",
    "--disable-ipc-flooding-protection",
    "--disable-popup-blocking",
    "--disable-prompt-on-repost",
    "--disable-renderer-backgrounding",
    "--disable-sync",
    "--enable-automation",
    "--force-color-profile=srgb",
    "--metrics-recording-only",
    "--no-first-run",
    "--password-store=basic",
    "--remote-debugging-port=0",
    "--use-mock-keychain",
    "--enable-blink-features=IdleDetection",
    "--headless",
    "--disable-gpu",
    "--hide-scrollbars",
    "--mute-audio",
]

WS_RE = re.compile(r"listening on (ws://[^ ]*)")


class ChromeClosedException(Exception):
    pass


class ChromeRunner:
    def __init__(self, proxy=None):
        super().__init__()

        self.proxy = proxy

        self.data_dir = tempfile.TemporaryDirectory()

        self.proc = None
        self.websocket_uri = None

    def __del__(self):
        """
        Kill the chrome we launched and all child processes
        """

        if self.proc and self.proc.pid:
            try:
                os.killpg(os.getpgid(self.proc.pid), signal.SIGKILL)

            except ProcessLookupError:
                pass

    async def launch(self, chrome_path=CHROME_PATH, extra_args=None):
        command = [chrome_path, *CHROME_PARAMS, f"--user-data-dir={self.data_dir.name}"]
        if extra_args:
            command += extra_args

        if self.proxy:
            command.append(f"--proxy-server={self.proxy}")

        self.proc = await asyncio.create_subprocess_exec(
            *command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            preexec_fn=os.setsid,
        )

        output = ""
        while True:
            if self.proc.returncode is not None:
                stderr = await self.proc.stdout.read()
                raise ChromeClosedException(
                    f"Chrome closed unexpectedly; code: {self.proc.returncode} ({stderr})"
                )

            data = await self.proc.stdout.readline()
            output += data.decode()

            search = WS_RE.search(output)
            if search:
                break

        self.websocket_uri = search.group(1).strip()
        LOGGER.info("Parsed websocket URI: %s", self.websocket_uri)
