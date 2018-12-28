from functools import wraps
from types import MethodType

import asyncio
import inspect
import logging
import types

import requests

from chrome import ChromeDevTools, ChromeRunner, ChromeDevToolsTarget


logger = logging.getLogger("cdipy.scripts.test")
logger.setLevel(10)
logging.basicConfig(format="[%(asctime)s] [%(levelname)s] %(message)s")
 

def printer(*args, **kwargs):
    print(f"{args}, {kwargs}")


async def main():
    protocol = requests.get("https://raw.githubusercontent.com/ChromeDevTools/devtools-protocol/master/json/browser_protocol.json").json()

    logger.debug("Generating objects for protocol version {0}.{1}".format(
        protocol["version"]["major"], protocol["version"]["minor"]))

    chrome = ChromeRunner()
    await chrome.launch()
    
    cdi = ChromeDevTools(chrome.websocket_uri, protocol)
    await cdi.connect()

    target = await cdi.Target.createTarget("about:blank")
    print(f"Target: {target}")

    session = await cdi.Target.attachToTarget(targetId=target["targetId"])
    print(f"Session: {session}")

    cdit = ChromeDevToolsTarget(cdi, session["sessionId"])
    print(f"cdit: {cdit}")

    await asyncio.gather(
        cdit.Network.enable(),
        cdit.Page.enable())

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
    
    await cdit.Page.navigate("https://google.com/")

    # cdit.on("Network.responseReceived", printer)

    await asyncio.sleep(10)



asyncio.get_event_loop().run_until_complete(main())
