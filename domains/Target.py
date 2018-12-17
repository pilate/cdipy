from .decorators import proxy_command


class Target(object):

    def __init__(self, devtools):
        self.devtools = devtools


    @proxy_command
    async def activateTarget(self, targetId):
        """
            Activates (focuses) the target.
        """

    @proxy_command
    async def attachToTarget(self, targetId, flatten=None):
        """
            Attaches to the target with given id.
        """


    @proxy_command
    async def attachToBrowserTarget(self):
        """
            Attaches to the browser target, only uses flat sessionId mode.
        """


    @proxy_command
    async def closeTarget(self, targetId):
        """
            Closes the target. If the target is a page that gets closed too.
        """


    @proxy_command
    async def exposeDevToolsProtocol(self, targetId, bindingName=None):
        """
            Inject object to the target's main frame that provides a communication
            channel with browser target.

            Injected object will be available as `window[bindingName]`.

            The object has the follwing API:
            - `binding.send(json)` - a method to send messages over the remote debugging protocol
            - `binding.onmessage = json => handleMessage(json)` - a callback that will be called for the protocol notifications and command responses.
        """


    @proxy_command
    async def createBrowserContext(self):
        """
            Creates a new empty BrowserContext. Similar to an incognito profile but you can have more than
            one.
        """


    @proxy_command
    async def getBrowserContexts(self):
        """
            Returns all browser contexts created with `Target.createBrowserContext` method.
        """


    @proxy_command
    async def createTarget(self, url, width=None, height=None, browserContextId=None, enableBeginFrameControl=None):
        """
            Creates a new page.
        """


    @proxy_command
    async def detachFromTarget(self, sessionId=None, targetId=None):
        """
            Detaches session with given id.
        """


    @proxy_command
    async def disposeBrowserContext(self, browserContextId):
        """
            Deletes a BrowserContext. All the belonging pages will be closed without calling their
            beforeunload hooks.
        """


    @proxy_command
    async def getTargetInfo(self, targetId=None):
        """
            Returns information about a target.
        """


    @proxy_command
    async def getTargets(self):
        """
            Retrieves a list of available targets.
        """


    @proxy_command
    async def sendMessageToTarget(self, message, sessionId=None, targetId=None):
        """
            Sends protocol message over session with given id.
        """


    @proxy_command
    async def setAutoAttach(self, autoAttach, waitForDebuggerOnStart, flatten=None):
        """
            Controls whether to automatically attach to new targets which are considered to be related to
            this one. When turned on, attaches to all existing related targets as well. When turned off,
            automatically detaches from all currently attached targets.
        """


    @proxy_command
    async def setDiscoverTargets(self, discover):
        """
            Controls whether to discover available targets and notify via
            `targetCreated/targetInfoChanged/targetDestroyed` events.
        """


    @proxy_command
    async def setRemoteLocations(self, locations):
        """
            Enables target discovery for the specified locations, when `setDiscoverTargets` was set to
            `true`.
        """

