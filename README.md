# cdipy
Chrome Devtools Interface that instruments Chrome via the [devtools protocol](https://github.com/ChromeDevTools/devtools-protocol).

Meant to serve as a pythonic version of [chrome-remote-interface](https://github.com/cyrus-and/chrome-remote-interface).

### Example Usage
```python

import asyncio
import base64
import logging
import sys

from cdipy import ChromeDevTools
from cdipy import ChromeDevToolsTarget
from cdipy import ChromeRunner


LOGGER = logging.getLogger("cdipy.scripts.screenshot")
FILENAME = "screenshot.png"


async def async_main(url):
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

    # Enable 'Page' events
    await cdit.Page.enable()

    # Navigate to URL
    LOGGER.info("Navigating to %s", url)
    await cdit.Page.navigate(url)

    # Wait for the Page.loadEventFired event
    # This may not ever fire on some pages, so it's good to set a limit
    try:
        await cdit.wait_for("Page.loadEventFired", 10)
    except asyncio.TimeoutError:
        print("Loaded event never fired!")

    # Take a screenshot
    screenshot_response = await cdit.Page.captureScreenshot(format="png")
    screenshot_bytes = base64.b64decode(screenshot_response["data"])

    with open(FILENAME, "w+b") as fileobj:
        fileobj.write(screenshot_bytes)

    LOGGER.info("wrote %s", FILENAME)


def main():
    logging.basicConfig(level=logging.INFO)

    asyncio.run(async_main(sys.argv[1]))


if __name__ == "__main__":
    main()


```
