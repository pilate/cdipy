import asyncio

from chrome import *


logger = logging.getLogger("cdt.test")
logging.basicConfig(format="[%(asctime)s] [%(levelname)s] %(message)s", level=logging.DEBUG)



async def main():
    cdt = ChromeDevTools()
    await cdt.launch()
    
    targets = await cdt.Target.getTargets()
    logger.info(f"getTargets result: {targets}")

    target = await cdt.Target.createTarget("about:blank")
    logger.info(f"createTarget result: {target}")

    session = await cdt.Target.attachToTarget(targetId=target["targetId"])
    logger.info(f"attach: {session}")

    await cdt.Page.enable()
    await cdt.Network.enable()
    await cdt.Page.navigate("https://google.com")
    await asyncio.sleep(5)
    import base64
    screenshot = base64.b64decode((await cdt.Page.captureScreenshot(format="png"))["data"])
    open("umf.png", "w+b").write(screenshot)
    await asyncio.sleep(10)


asyncio.get_event_loop().run_until_complete(main())



"""



class attribattrib(object):
    def __getattribute__(self,  attrib):
        print(attrib)


a = attribattrib()
a.Test.thing



"""