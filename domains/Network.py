from .decorators import proxy_target_command



class Network(object):

    def __init__(self, devtools):
        self.devtools = devtools


    @proxy_target_command
    async def canClearBrowserCache(self):
        """
            Tells whether clearing browser cache is supported.
        """


    @proxy_target_command
    async def canClearBrowserCookies(self):
        """
            Tells whether clearing browser cookies is supported.
        """


    @proxy_target_command
    async def canEmulateNetworkConditions(self):
        """
            Tells whether emulation of network conditions is supported.
        """


    @proxy_target_command
    async def clearBrowserCache(self):
        """
            Clears browser cache.
        """


    @proxy_target_command
    async def clearBrowserCookies(self):
        """
            Clears browser cookies.
        """


    @proxy_target_command
    async def continueInterceptedRequest(self, interceptionId, errorReason=None, rawResponse=None, url=None, method=None, postData=None, headers=None, authChallengeResponse=None):
        """
            Response to Network.requestIntercepted which either modifies the request to continue with any
modifications, or blocks it, or completes it with the provided response bytes. If a network
fetch occurs as a result which encounters a redirect an additional Network.requestIntercepted
event will be sent with the same InterceptionId.
        """


    @proxy_target_command
    async def deleteCookies(self, name, url=None, domain=None, path=None):
        """
            Deletes browser cookies with matching name and url or domain/path pair.
        """


    @proxy_target_command
    async def disable(self):
        """
            Disables network tracking, prevents network events from being sent to the client.
        """


    @proxy_target_command
    async def emulateNetworkConditions(self, offline, latency, downloadThroughput, uploadThroughput, connectionType=None):
        """
            Activates emulation of network conditions.
        """


    @proxy_target_command
    async def enable(self, maxTotalBufferSize=None, maxResourceBufferSize=None, maxPostDataSize=None):
        """
            Enables network tracking, network events will now be delivered to the client.
        """


    @proxy_target_command
    async def getAllCookies(self):
        """
            Returns all browser cookies. Depending on the backend support, will return detailed cookie
information in the `cookies` field.
        """


    @proxy_target_command
    async def getCertificate(self, origin):
        """
            Returns the DER-encoded certificate.
        """


    @proxy_target_command
    async def getCookies(self, urls=None):
        """
            Returns all browser cookies for the current URL. Depending on the backend support, will return
detailed cookie information in the `cookies` field.
        """


    @proxy_target_command
    async def getResponseBody(self, requestId):
        """
            Returns content served for the given request.
        """


    @proxy_target_command
    async def getRequestPostData(self, requestId):
        """
            Returns post data sent with the request. Returns an error when no data was sent with the request.
        """


    @proxy_target_command
    async def getResponseBodyForInterception(self, interceptionId):
        """
            Returns content served for the given currently intercepted request.
        """


    @proxy_target_command
    async def takeResponseBodyForInterceptionAsStream(self, interceptionId):
        """
            Returns a handle to the stream representing the response body. Note that after this command,
the intercepted request can't be continued as is -- you either need to cancel it or to provide
the response body. The stream only supports sequential read, IO.read will fail if the position
is specified.
        """


    @proxy_target_command
    async def replayXHR(self, requestId):
        """
            This method sends a new XMLHttpRequest which is identical to the original one. The following
parameters should be identical: method, url, async, request body, extra headers, withCredentials
attribute, user, password.
        """


    @proxy_target_command
    async def searchInResponseBody(self, requestId, query, caseSensitive=None, isRegex=None):
        """
            Searches for given string in response content.
        """


    @proxy_target_command
    async def setBlockedURLs(self, urls):
        """
            Blocks URLs from loading.
        """


    @proxy_target_command
    async def setBypassServiceWorker(self, bypass):
        """
            Toggles ignoring of service worker for each request.
        """


    @proxy_target_command
    async def setCacheDisabled(self, cacheDisabled):
        """
            Toggles ignoring cache for each request. If `true`, cache will not be used.
        """


    @proxy_target_command
    async def setCookie(self, name, value, url=None, domain=None, path=None, secure=None, httpOnly=None, sameSite=None, expires=None):
        """
            Sets a cookie with the given cookie data; may overwrite equivalent cookies if they exist.
        """


    @proxy_target_command
    async def setCookies(self, cookies):
        """
            Sets given cookies.
        """


    @proxy_target_command
    async def setDataSizeLimitsForTest(self, maxTotalSize, maxResourceSize):
        """
            For testing.
        """


    @proxy_target_command
    async def setExtraHTTPHeaders(self, headers):
        """
            Specifies whether to always send extra HTTP headers with the requests from this page.
        """


    @proxy_target_command
    async def setRequestInterception(self, patterns):
        """
            Sets the requests to intercept that match a the provided patterns and optionally resource types.
        """


    @proxy_target_command
    async def setUserAgentOverride(self, userAgent, acceptLanguage=None, platform=None):
        """
            Allows overriding user agent with the given string.
        """

