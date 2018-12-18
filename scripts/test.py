import asyncio
import base64
import logging

from chrome import ChromeDevTools


logger = logging.getLogger("cdipy.scripts.test")
logging.basicConfig(format="[%(asctime)s] [%(levelname)s] %(message)s", level=logging.DEBUG)



async def main():
    cdt = ChromeDevTools()
    await cdt.launch()

    target = await cdt.Target.createTarget("about:blank")
    session = await cdt.Target.attachToTarget(targetId=target["targetId"])

    await cdt.Page.enable()
    await cdt.Network.enable()
    await cdt.Page.navigate("https://google.com")

    await asyncio.sleep(5)

    ss_response = await cdt.Page.captureScreenshot(format="png")
    screenshot = base64.b64decode(ss_response["data"])
    open("google.png", "w+b").write(screenshot)
    
    await asyncio.sleep(10)


asyncio.get_event_loop().run_until_complete(main())
