from .decorators import proxy_target_command



class DOMSnapshot(object):

    def __init__(self, devtools):
        self.devtools = devtools


    @proxy_target_command
    async def disable(self):
        """
            Disables DOM snapshot agent for the given page.
        """


    @proxy_target_command
    async def enable(self):
        """
            Enables DOM snapshot agent for the given page.
        """


    @proxy_target_command
    async def getSnapshot(self, computedStyleWhitelist, includeEventListeners=None, includePaintOrder=None, includeUserAgentShadowTree=None):
        """
            Returns a document snapshot, including the full DOM tree of the root node (including iframes,
template contents, and imported documents) in a flattened array, as well as layout and
white-listed computed style information for the nodes. Shadow DOM in the returned DOM tree is
flattened.
        """


    @proxy_target_command
    async def captureSnapshot(self, computedStyles):
        """
            Returns a document snapshot, including the full DOM tree of the root node (including iframes,
template contents, and imported documents) in a flattened array, as well as layout and
white-listed computed style information for the nodes. Shadow DOM in the returned DOM tree is
flattened.
        """

