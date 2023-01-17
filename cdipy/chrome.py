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


DEFAULT_ARGS = [
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

CHROME_PATH = "/usr/bin/google-chrome-stable"
WS_RE = re.compile(r"listening on (ws://[^ ]*)")


class ChromeClosedException(Exception):
    pass


class ChromeRunner:
    def __init__(self, proxy=None, tmp_path=None):
        super().__init__()

        self.proxy = proxy

        if tmp_path:
            self.tmp_path = tmp_path
        else:
            self.tmp_path = Path(tempfile.mkdtemp())

        self.proc = None
        self.proc_pid = None
        self.websocket_uri = None

    # Browser cleanup
    def __del__(self):
        # Kill chrome and all of its child processes
        if self.proc_pid:
            try:
                os.killpg(os.getpgid(self.proc_pid), signal.SIGKILL)

            except ProcessLookupError:
                pass

        # Empty the user data directory
        shutil.rmtree(self.tmp_path, ignore_errors=True)

    async def launch(self, chrome_path=CHROME_PATH, extra_args=None):
        command = [chrome_path] + DEFAULT_ARGS + [f"--user-data-dir={self.tmp_path}"]

        if extra_args:
            command += extra_args

        if self.proxy:
            command += [f"--proxy-server={self.proxy}"]

        self.proc = await asyncio.create_subprocess_exec(
            *command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            preexec_fn=os.setsid,
        )
        self.proc_pid = self.proc.pid

        output = ""
        while True:
            if self.proc.returncode is not None:
                stderr = await self.proc.stdout.read()
                raise ChromeClosedException(
                    f"Chrome closed unexpectedly with return code: {self.proc.returncode} ({stderr})"
                )

            data = await self.proc.stdout.readline()
            output += data.decode()

            search = WS_RE.search(output)
            if search:
                break

        self.websocket_uri = search.group(1).strip()
        LOGGER.info("Parsed websocket URI: %s", self.websocket_uri)
