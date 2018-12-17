from .decorators import proxy_target_command



class Emulation(object):

    def __init__(self, devtools):
        self.devtools = devtools


    @proxy_target_command
    async def canEmulate(self):
        """
            Tells whether emulation is supported.
        """


    @proxy_target_command
    async def clearDeviceMetricsOverride(self):
        """
            Clears the overriden device metrics.
        """


    @proxy_target_command
    async def clearGeolocationOverride(self):
        """
            Clears the overriden Geolocation Position and Error.
        """


    @proxy_target_command
    async def resetPageScaleFactor(self):
        """
            Requests that page scale factor is reset to initial values.
        """


    @proxy_target_command
    async def setFocusEmulationEnabled(self, enabled):
        """
            Enables or disables simulating a focused and active page.
        """


    @proxy_target_command
    async def setCPUThrottlingRate(self, rate):
        """
            Enables CPU throttling to emulate slow CPUs.
        """


    @proxy_target_command
    async def setDefaultBackgroundColorOverride(self, color=None):
        """
            Sets or clears an override of the default background color of the frame. This override is used
if the content does not specify one.
        """


    @proxy_target_command
    async def setDeviceMetricsOverride(self, width, height, deviceScaleFactor, mobile, scale=None, screenWidth=None, screenHeight=None, positionX=None, positionY=None, dontSetVisibleSize=None, screenOrientation=None, viewport=None):
        """
            Overrides the values of device screen dimensions (window.screen.width, window.screen.height,
window.innerWidth, window.innerHeight, and "device-width"/"device-height"-related CSS media
query results).
        """


    @proxy_target_command
    async def setScrollbarsHidden(self, hidden):
        """
            None
        """


    @proxy_target_command
    async def setDocumentCookieDisabled(self, disabled):
        """
            None
        """


    @proxy_target_command
    async def setEmitTouchEventsForMouse(self, enabled, configuration=None):
        """
            None
        """


    @proxy_target_command
    async def setEmulatedMedia(self, media):
        """
            Emulates the given media for CSS media queries.
        """


    @proxy_target_command
    async def setGeolocationOverride(self, latitude=None, longitude=None, accuracy=None):
        """
            Overrides the Geolocation Position or Error. Omitting any of the parameters emulates position
unavailable.
        """


    @proxy_target_command
    async def setNavigatorOverrides(self, platform):
        """
            Overrides value returned by the javascript navigator object.
        """


    @proxy_target_command
    async def setPageScaleFactor(self, pageScaleFactor):
        """
            Sets a specified page scale factor.
        """


    @proxy_target_command
    async def setScriptExecutionDisabled(self, value):
        """
            Switches script execution in the page.
        """


    @proxy_target_command
    async def setTouchEmulationEnabled(self, enabled, maxTouchPoints=None):
        """
            Enables touch on platforms which do not support them.
        """


    @proxy_target_command
    async def setVirtualTimePolicy(self, policy, budget=None, maxVirtualTimeTaskStarvationCount=None, waitForNavigation=None, initialVirtualTime=None):
        """
            Turns on virtual time for all frames (replacing real-time with a synthetic time source) and sets
the current virtual time policy.  Note this supersedes any previous time budget.
        """


    @proxy_target_command
    async def setVisibleSize(self, width, height):
        """
            Resizes the frame/viewport of the page. Note that this does not affect the frame's container
(e.g. browser window). Can be used to produce screenshots of the specified size. Not supported
on Android.
        """


    @proxy_target_command
    async def setUserAgentOverride(self, userAgent, acceptLanguage=None, platform=None):
        """
            Allows overriding user agent with the given string.
        """

