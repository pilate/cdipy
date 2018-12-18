from .decorators import proxy_target_command



class Page(object):

    def __init__(self, devtools):
        self.devtools = devtools


    @proxy_target_command
    async def addScriptToEvaluateOnLoad(self, scriptSource):
        """
            Deprecated, please use addScriptToEvaluateOnNewDocument instead.
        """


    @proxy_target_command
    async def addScriptToEvaluateOnNewDocument(self, source, worldName=None):
        """
            Evaluates given script in every frame upon creation (before loading frame's scripts).
        """


    @proxy_target_command
    async def bringToFront(self):
        """
            Brings page to front (activates tab).
        """


    @proxy_target_command
    async def captureScreenshot(self, format=None, quality=None, clip=None, fromSurface=None):
        """
            Capture page screenshot.
        """


    @proxy_target_command
    async def captureSnapshot(self, format=None):
        """
            Returns a snapshot of the page as a string. For MHTML format, the serialization includes
            iframes, shadow DOM, external resources, and element-inline styles.
        """


    @proxy_target_command
    async def clearDeviceMetricsOverride(self):
        """
            Clears the overriden device metrics.
        """


    @proxy_target_command
    async def clearDeviceOrientationOverride(self):
        """
            Clears the overridden Device Orientation.
        """


    @proxy_target_command
    async def clearGeolocationOverride(self):
        """
            Clears the overriden Geolocation Position and Error.
        """


    @proxy_target_command
    async def createIsolatedWorld(self, frameId, worldName=None, grantUniveralAccess=None):
        """
            Creates an isolated world for the given frame.
        """


    @proxy_target_command
    async def deleteCookie(self, cookieName, url):
        """
            Deletes browser cookie with given name, domain and path.
        """


    @proxy_target_command
    async def disable(self):
        """
            Disables page domain notifications.
        """


    @proxy_target_command
    async def enable(self):
        """
            Enables page domain notifications.
        """


    @proxy_target_command
    async def getAppManifest(self):
        """
            None
        """


    @proxy_target_command
    async def getCookies(self):
        """
            Returns all browser cookies. Depending on the backend support, will return detailed cookie
            information in the `cookies` field.
        """


    @proxy_target_command
    async def getFrameTree(self):
        """
            Returns present frame tree structure.
        """


    @proxy_target_command
    async def getLayoutMetrics(self):
        """
            Returns metrics relating to the layouting of the page, such as viewport bounds/scale.
        """


    @proxy_target_command
    async def getNavigationHistory(self):
        """
            Returns navigation history for the current page.
        """


    @proxy_target_command
    async def resetNavigationHistory(self):
        """
            Resets navigation history for the current page.
        """


    @proxy_target_command
    async def getResourceContent(self, frameId, url):
        """
            Returns content of the given resource.
        """


    @proxy_target_command
    async def getResourceTree(self):
        """
            Returns present frame / resource tree structure.
        """


    @proxy_target_command
    async def handleJavaScriptDialog(self, accept, promptText=None):
        """
            Accepts or dismisses a JavaScript initiated dialog (alert, confirm, prompt, or onbeforeunload).
        """


    @proxy_target_command
    async def navigate(self, url, referrer=None, transitionType=None, frameId=None):
        """
            Navigates current page to the given URL.
        """


    @proxy_target_command
    async def navigateToHistoryEntry(self, entryId):
        """
            Navigates current page to the given history entry.
        """


    @proxy_target_command
    async def printToPDF(self, landscape=None, displayHeaderFooter=None, printBackground=None, scale=None, paperWidth=None, paperHeight=None, marginTop=None, marginBottom=None, marginLeft=None, marginRight=None, pageRanges=None, ignoreInvalidPageRanges=None, headerTemplate=None, footerTemplate=None, preferCSSPageSize=None):
        """
            Print page as PDF.
        """


    @proxy_target_command
    async def reload(self, ignoreCache=None, scriptToEvaluateOnLoad=None):
        """
            Reloads given page optionally ignoring the cache.
        """


    @proxy_target_command
    async def removeScriptToEvaluateOnLoad(self, identifier):
        """
            Deprecated, please use removeScriptToEvaluateOnNewDocument instead.
        """


    @proxy_target_command
    async def removeScriptToEvaluateOnNewDocument(self, identifier):
        """
            Removes given script from the list.
        """


    @proxy_target_command
    async def requestAppBanner(self):
        """
            None
        """


    @proxy_target_command
    async def screencastFrameAck(self, sessionId):
        """
            Acknowledges that a screencast frame has been received by the frontend.
        """


    @proxy_target_command
    async def searchInResource(self, frameId, url, query, caseSensitive=None, isRegex=None):
        """
            Searches for given string in resource content.
        """


    @proxy_target_command
    async def setAdBlockingEnabled(self, enabled):
        """
            Enable Chrome's experimental ad filter on all sites.
        """


    @proxy_target_command
    async def setBypassCSP(self, enabled):
        """
            Enable page Content Security Policy by-passing.
        """


    @proxy_target_command
    async def setDeviceMetricsOverride(self, width, height, deviceScaleFactor, mobile, scale=None, screenWidth=None, screenHeight=None, positionX=None, positionY=None, dontSetVisibleSize=None, screenOrientation=None, viewport=None):
        """
            Overrides the values of device screen dimensions (window.screen.width, window.screen.height,
            window.innerWidth, window.innerHeight, and "device-width"/"device-height"-related CSS media
            query results).
        """


    @proxy_target_command
    async def setDeviceOrientationOverride(self, alpha, beta, gamma):
        """
            Overrides the Device Orientation.
        """


    @proxy_target_command
    async def setFontFamilies(self, fontFamilies):
        """
            Set generic font families.
        """


    @proxy_target_command
    async def setFontSizes(self, fontSizes):
        """
            Set default font sizes.
        """


    @proxy_target_command
    async def setDocumentContent(self, frameId, html):
        """
            Sets given markup as the document's HTML.
        """


    @proxy_target_command
    async def setDownloadBehavior(self, behavior, downloadPath=None):
        """
            Set the behavior when downloading a file.
        """


    @proxy_target_command
    async def setGeolocationOverride(self, latitude=None, longitude=None, accuracy=None):
        """
            Overrides the Geolocation Position or Error. Omitting any of the parameters emulates position
            unavailable.
        """


    @proxy_target_command
    async def setLifecycleEventsEnabled(self, enabled):
        """
            Controls whether page will emit lifecycle events.
        """


    @proxy_target_command
    async def setTouchEmulationEnabled(self, enabled, configuration=None):
        """
            Toggles mouse event-based touch event emulation.
        """


    @proxy_target_command
    async def startScreencast(self, format=None, quality=None, maxWidth=None, maxHeight=None, everyNthFrame=None):
        """
            Starts sending each frame using the `screencastFrame` event.
        """


    @proxy_target_command
    async def stopLoading(self):
        """
            Force the page stop all navigations and pending resource fetches.
        """


    @proxy_target_command
    async def crash(self):
        """
            Crashes renderer on the IO thread, generates minidumps.
        """


    @proxy_target_command
    async def close(self):
        """
            Tries to close page, running its beforeunload hooks, if any.
        """


    @proxy_target_command
    async def setWebLifecycleState(self, state):
        """
            Tries to update the web lifecycle state of the page.
            It will transition the page to the given state according to:
            https://github.com/WICG/web-lifecycle/
        """


    @proxy_target_command
    async def stopScreencast(self):
        """
            Stops sending each frame in the `screencastFrame`.
        """


    @proxy_target_command
    async def setProduceCompilationCache(self, enabled):
        """
            Forces compilation cache to be generated for every subresource script.
        """


    @proxy_target_command
    async def addCompilationCache(self, url, data):
        """
            Seeds compilation cache for given url. Compilation cache does not survive
            cross-process navigation.
        """


    @proxy_target_command
    async def clearCompilationCache(self):
        """
            Clears seeded compilation cache.
        """


    @proxy_target_command
    async def generateTestReport(self, message, group=None):
        """
            Generates a report for testing.
        """


    @proxy_target_command
    async def waitForDebugger(self):
        """
            Pauses page execution. Can be resumed using generic Runtime.runIfWaitingForDebugger.
        """

