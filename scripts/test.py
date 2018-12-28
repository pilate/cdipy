from functools import wraps
from types import MethodType

import asyncio
import base64
import inspect
import logging
import types

import requests

from cdipy import ChromeDevTools
from cdipy import ChromeDevToolsTarget
from cdipy import ChromeRunner


logger = logging.getLogger("cdipy.scripts.test")
logger.setLevel(10)
logging.basicConfig(format="[%(asctime)s] [%(levelname)s] %(message)s")
 

async def main():

    domains = []
    protocol = requests.get("https://raw.githubusercontent.com/ChromeDevTools/devtools-protocol/master/json/browser_protocol.json").json()
    domains += protocol["domains"]

    protocol = requests.get("https://raw.githubusercontent.com/ChromeDevTools/devtools-protocol/master/json/js_protocol.json").json()
    domains += protocol["domains"]
    
    logger.debug("Generating objects for protocol version {0}.{1}".format(
        protocol["version"]["major"], protocol["version"]["minor"]))

    chrome = ChromeRunner()
    await chrome.launch()
    
    cdi = ChromeDevTools(chrome.websocket_uri, domains)
    await cdi.connect()

    target = await cdi.Target.createTarget("about:blank")
    print(f"Target: {target}")

    session = await cdi.Target.attachToTarget(targetId=target["targetId"])
    print(f"Session: {session}")

    cdit = ChromeDevToolsTarget(cdi, session["sessionId"])

    await asyncio.gather(
        cdit.Network.enable(),
        cdit.Page.enable(),
        cdit.Runtime.enable(),
        cdit.Debugger.enable(),
        cdit.Security.enable(),
        cdit.Page.setDownloadBehavior(behavior="allow", downloadPath=str(chrome.tmp_path)))

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
   
    await cdit.Page.navigate("https://ultramusicfestival.com/")

    await asyncio.sleep(10)

    screenshot_response = await cdit.Page.captureScreenshot(format="png")
    screenshot_bytes = base64.b64decode(screenshot_response["data"])
    open("screenshot.png", "w+b").write(screenshot_bytes)



asyncio.get_event_loop().run_until_complete(main())
