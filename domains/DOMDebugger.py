from .decorators import proxy_target_command



class DOMDebugger(object):

    def __init__(self, devtools):
        self.devtools = devtools


    @proxy_target_command
    async def getEventListeners(self, objectId, depth=None, pierce=None):
        """
            Returns event listeners of the given object.
        """


    @proxy_target_command
    async def removeDOMBreakpoint(self, nodeId, type):
        """
            Removes DOM breakpoint that was set using `setDOMBreakpoint`.
        """


    @proxy_target_command
    async def removeEventListenerBreakpoint(self, eventName, targetName=None):
        """
            Removes breakpoint on particular DOM event.
        """


    @proxy_target_command
    async def removeInstrumentationBreakpoint(self, eventName):
        """
            Removes breakpoint on particular native event.
        """


    @proxy_target_command
    async def removeXHRBreakpoint(self, url):
        """
            Removes breakpoint from XMLHttpRequest.
        """


    @proxy_target_command
    async def setDOMBreakpoint(self, nodeId, type):
        """
            Sets breakpoint on particular operation with DOM.
        """


    @proxy_target_command
    async def setEventListenerBreakpoint(self, eventName, targetName=None):
        """
            Sets breakpoint on particular DOM event.
        """


    @proxy_target_command
    async def setInstrumentationBreakpoint(self, eventName):
        """
            Sets breakpoint on particular native event.
        """


    @proxy_target_command
    async def setXHRBreakpoint(self, url):
        """
            Sets breakpoint on XMLHttpRequest.
        """

