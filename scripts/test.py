import asyncio
import logging

from cdipy import ChromeDevTools
from cdipy import ChromeDevToolsTarget
from cdipy import ChromeRunner


LOGGER = logging.getLogger("cdipy.scripts.test")
logging.basicConfig(
    format="[%(name)s:%(funcName)s:%(lineno)s] %(message)s", level=logging.DEBUG
)

logging.getLogger("websockets").setLevel(logging.ERROR)
logging.getLogger("cdipy").setLevel(logging.INFO)


async def crawl(url):
    # Start Chrome
    chrome = ChromeRunner()
    await chrome.launch()

    # Connect to devtools websocket
    cdi = ChromeDevTools(chrome.websocket_uri)
    await cdi.connect()

    # Create a new target and attach to it
    target = await cdi.Target.createTarget("about:blank")
    session = await cdi.Target.attachToTarget(targetId=target["targetId"])

    # Create a ChromeDevToolsTarget class to handle target messages
    cdit = ChromeDevToolsTarget(cdi, session["sessionId"])

    await asyncio.gather(
        cdit.Network.enable(),
        cdit.Page.enable(),
        cdit.Runtime.enable(),
        cdit.Debugger.enable(),
        cdit.Security.enable(),
        cdit.Page.setDownloadBehavior(
            behavior="allow", downloadPath=str(chrome.tmp_path)
        ),
    )

    # await asyncio.gather(
    #     cdit.Animation.enable(),
    #     cdit.DOM.enable(),
    #     cdit.DOMSnapshot.enable(),
    #     cdit.DOMStorage.enable(),
    #     cdit.Database.enable(),
    #     cdit.HeadlessExperimental.enable(),
    #     cdit.IndexedDB.enable(),
    #     cdit.Inspector.enable(),
    #     cdit.LayerTree.enable(),
    #     cdit.Log.enable(),
    #     cdit.Network.enable(),
    #     cdit.Overlay.enable(),
    #     cdit.Page.enable(),
    #     cdit.Performance.enable(),
    #     cdit.Security.enable(),
    #     cdit.ServiceWorker.enable())

    # await asyncio.gather(
    #     cdit.DOMDebugger.setXHRBreakpoint("http"),
    #     cdit.Tracing.start())

    # await cdi.Tethering.bind(9999)

    # def printer(*args, **kwargs):
    #     print(f"{args}, {kwargs}")
    #
    # cdit.on("Network.responseReceived", printer)

    await cdit.Emulation.setDeviceMetricsOverride(
        width=1024, height=768, deviceScaleFactor=0, mobile=False
    )

    await cdit.Page.navigate(url)

    await asyncio.sleep(5)

    screenshot_response = await cdit.Page.captureScreenshot(format="png")
    # screenshot_bytes = base64.b64decode(screenshot_response["data"])
    # open("screenshot.png", "w+b").write(screenshot_bytes)


async def main():
    await crawl("http://google.com/")


asyncio.run(main())
