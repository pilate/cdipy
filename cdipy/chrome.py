import asyncio
import logging
import os
import signal
from asyncio import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

from .exceptions import ChromeClosedException


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
    "--disable-component-update",
    "--disable-default-apps",
    "--disable-domain-reliability",
    "--disable-extensions",
    "--disable-features=CalculateNativeWinOcclusion,InterestFeedContentSuggestions,Translate",
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
    "--ash-no-nudges",
    "--disable-search-engine-choice-screen",
    "--propagate-iph-for-testing",
    "--no-default-browser-check",
    "--password-store=basic",
    "--remote-debugging-port=0",
    "--use-mock-keychain",
    "--enable-blink-features=IdleDetection",
    "--disable-gpu",
    "--hide-scrollbars",
    "--mute-audio",
    # only log FATAL to cut console-echo spam; log-level is only honored
    # when the logging destination is set explicitly
    "--enable-logging=stderr",
    "--log-level=3",
]
if not os.environ.get("CDIPY_USE_SHM"):
    CHROME_PARAMS.append("--disable-dev-shm-usage")


class ChromeRunner:
    def __init__(self, proxy: str = None, ignore_cleanup_errors=False):
        super().__init__()

        self.proxy = proxy

        self.data_dir = TemporaryDirectory(
            ignore_cleanup_errors=ignore_cleanup_errors
        )  # pylint: disable=consider-using-with

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

    async def launch(
        self,
        chrome_path: str = CHROME_PATH,
        extra_args: list = None,
        headless: str = "new",
        log_output: bool = False,
    ) -> None:
        command = [
            chrome_path,
            *CHROME_PARAMS,
            f"--headless={headless}",
            f"--user-data-dir={self.data_dir.name}",
        ]

        if extra_args:
            command.extend(extra_args)

        if self.proxy:
            command.append(f"--proxy-server={self.proxy}")

        # Discard chrome's output by default; never use a pipe, an unread
        # pipe eventually fills and blocks chrome entirely
        output = subprocess.DEVNULL
        if log_output:
            output = open(os.path.join(self.data_dir.name, "chrome.log"), "wb")

        try:
            self.proc = await asyncio.create_subprocess_exec(
                *command,
                stdout=output,
                stderr=subprocess.STDOUT,
                preexec_fn=os.setsid,
            )
        finally:
            if log_output:
                output.close()

        # Chrome writes the devtools port and browser target path to
        # DevToolsActivePort in the data dir once the listener is ready
        port_path = Path(self.data_dir.name) / "DevToolsActivePort"
        while True:
            # the average time chrome was observed to take (46-54ms)
            await asyncio.sleep(0.05)

            if self.proc.returncode is not None:
                log_tail = ""
                if log_output:
                    with open(output.name, "rb") as log_file:
                        log_file.seek(0, os.SEEK_END)
                        log_file.seek(max(log_file.tell() - 2048, 0))
                        log_tail = log_file.read()

                raise ChromeClosedException(
                    f"Chrome closed unexpectedly; code: {self.proc.returncode} ({log_tail})"
                )

            try:
                port, browser_path = port_path.read_text().splitlines()[:2]
                break
            except (FileNotFoundError, ValueError):
                pass

        self.websocket_uri = f"ws://127.0.0.1:{port}{browser_path}"
        LOGGER.info("Parsed websocket URI: %s", self.websocket_uri)
