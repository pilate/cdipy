from .decorators import proxy_target_command, proxy_command


class Browser(object):

    def __init__(self, devtools):
        self.devtools = devtools


    async def grantPermissions(self, origin, permissions, browserContextId=None):
        """
            Grant specific permissions to the given origin and reject all others.
        """


    async def resetPermissions(self, browserContextId=None):
        """
            Reset all permission management for all origins.
        """


    @proxy_command
    async def close(self):
        """
            Close browser gracefully.
        """


    async def crash(self):
        """
            Crashes browser on the main thread.
        """


    async def getVersion(self):
        """
            Returns version information.
        """


    async def getBrowserCommandLine(self):
        """
            Returns the command line switches for the browser process if, and only if
--enable-automation is on the commandline.
        """


    async def getHistograms(self, query=None, delta=None):
        """
            Get Chrome histograms.
        """


    async def getHistogram(self, name, delta=None):
        """
            Get a Chrome histogram by name.
        """


    async def getWindowBounds(self, windowId):
        """
            Get position and size of the browser window.
        """


    async def getWindowForTarget(self, targetId=None):
        """
            Get the browser window that contains the devtools target.
        """


    async def setWindowBounds(self, windowId, bounds):
        """
            Set position and/or size of the browser window.
        """


    async def setDockTile(self, badgeLabel=None, image=None):
        """
            Set dock tile details, platform-specific.
        """

