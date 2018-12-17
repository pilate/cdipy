from .decorators import proxy_target_command



class Accessibility(object):

    def __init__(self, devtools):
        self.devtools = devtools


    @proxy_target_command
    async def disable(self):
        """
            Disables the accessibility domain.
        """


    @proxy_target_command
    async def enable(self):
        """
            Enables the accessibility domain which causes `AXNodeId`s to remain consistent between method calls.
This turns on accessibility for the page, which can impact performance until accessibility is disabled.
        """


    @proxy_target_command
    async def getPartialAXTree(self, nodeId=None, backendNodeId=None, objectId=None, fetchRelatives=None):
        """
            Fetches the accessibility node and partial accessibility tree for this DOM node, if it exists.
        """


    @proxy_target_command
    async def getFullAXTree(self):
        """
            Fetches the entire accessibility tree
        """

