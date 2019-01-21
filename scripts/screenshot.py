import asyncio
import base64
import logging

from cdipy import ChromeDevTools
from cdipy import ChromeDevToolsTarget
from cdipy import ChromeRunner


logger = logging.getLogger(__name__)
 

async def main():
    # Start Chrome
    chrome = ChromeRunner()
    await chrome.launch()
    
    # Connect to Chrome
    cdi = ChromeDevTools(chrome.websocket_uri)
    await cdi.connect()

    # Create a new target and attach to it
    target = await cdi.Target.createTarget("about:blank")
    session = await cdi.Target.attachToTarget(targetId=target["targetId"])

    # Create a ChromeDevToolsTarget class to handle target messages
    cdit = ChromeDevToolsTarget(cdi, session["sessionId"])

    # Enable 'Page' events
    await cdit.Page.enable()

    # Navigate to URL
    await cdit.Page.navigate("https://google.com/")

    # Wait for the Page.loadEventFired event
    # This may not ever fire on some pages, so it's good to set a limit
    try:
        await cdit.wait_for("Page.loadEventFired", 10)
    except asyncio.TimeoutError:
        logger.warn("Loaded event never fired")

    # Take a screenshot
    screenshot_response = await cdit.Page.captureScreenshot(format="png")
    screenshot_bytes = base64.b64decode(screenshot_response["data"])
    open("screenshot.png", "w+b").write(screenshot_bytes)


asyncio.get_event_loop().run_until_complete(main())
