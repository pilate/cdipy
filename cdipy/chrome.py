from pathlib import Path

import asyncio
import asyncio.subprocess as subprocess
import logging
import os
import re
import shutil
import signal
import tempfile



logger = logging.getLogger("cdipy.chrome")
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


class ChromeRunner(object):

    def __init__(self, proxy=None, tmp_path=None):
        super().__init__()

        self.proxy = proxy

        if tmp_path:
            self.tmp_path = tmp_path
        else:
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