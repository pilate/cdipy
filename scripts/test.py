import asyncio
import base64
import logging

from cdipy import ChromeDevTools
from cdipy import ChromeDevToolsTarget
from cdipy import ChromeRunner


logger = logging.getLogger(__name__)
logging.getLogger("websockets").setLevel(logging.ERROR)


async def main():
    chrome = ChromeRunner()
    await chrome.launch()
    
    cdi = ChromeDevTools(chrome.websocket_uri)
    await cdi.connect()

    target = await cdi.Target.createTarget("about:blank")
    print(f"Target: {target}")

    session = await cdi.Target.attachToTarget(targetId=target["targetId"])
    print(f"Session: {session}")

    cdit = ChromeDevToolsTarget(cdi, session["sessionId"])
    await cdit.wait_for("Page.loadEventFired")

    # await asyncio.gather(
    #     cdit.Network.enable(),
    #     cdit.Page.enable(),
    #     cdit.Runtime.enable(),
    #     cdit.Debugger.enable(),
    #     cdit.Security.enable(),
    #     cdit.Page.setDownloadBehavior(behavior="allow", downloadPath=str(chrome.tmp_path)))

    # await asyncio.gather(
    #     cdit.Animation.enable(),
    #     cdit.ApplicationCache.enable(),
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

    await cdit.Emulation.setDeviceMetricsOverride(width=1024, height=768, deviceScaleFactor=0, mobile=False)
    await cdit.Network.setUserAgentOverride(userAgent="Definitely not headless Chrome")
   
    await cdit.Page.navigate("https://google.com/")

    await asyncio.sleep(10)

    screenshot_response = await cdit.Page.captureScreenshot(format="png")
    screenshot_bytes = base64.b64decode(screenshot_response["data"])
    open("screenshot.png", "w+b").write(screenshot_bytes)



asyncio.get_event_loop().run_until_complete(main())
