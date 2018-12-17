from .decorators import proxy_target_command



class Overlay(object):

    def __init__(self, devtools):
        self.devtools = devtools


    @proxy_target_command
    async def disable(self):
        """
            Disables domain notifications.
        """


    @proxy_target_command
    async def enable(self):
        """
            Enables domain notifications.
        """


    @proxy_target_command
    async def getHighlightObjectForTest(self, nodeId):
        """
            For testing.
        """


    @proxy_target_command
    async def hideHighlight(self):
        """
            Hides any highlight.
        """


    @proxy_target_command
    async def highlightFrame(self, frameId, contentColor=None, contentOutlineColor=None):
        """
            Highlights owner element of the frame with given id.
        """


    @proxy_target_command
    async def highlightNode(self, highlightConfig, nodeId=None, backendNodeId=None, objectId=None):
        """
            Highlights DOM node with given id or with the given JavaScript object wrapper. Either nodeId or
objectId must be specified.
        """


    @proxy_target_command
    async def highlightQuad(self, quad, color=None, outlineColor=None):
        """
            Highlights given quad. Coordinates are absolute with respect to the main frame viewport.
        """


    @proxy_target_command
    async def highlightRect(self, x, y, width, height, color=None, outlineColor=None):
        """
            Highlights given rectangle. Coordinates are absolute with respect to the main frame viewport.
        """


    @proxy_target_command
    async def setInspectMode(self, mode, highlightConfig=None):
        """
            Enters the 'inspect' mode. In this mode, elements that user is hovering over are highlighted.
Backend then generates 'inspectNodeRequested' event upon element selection.
        """


    @proxy_target_command
    async def setPausedInDebuggerMessage(self, message=None):
        """
            None
        """


    @proxy_target_command
    async def setShowDebugBorders(self, show):
        """
            Requests that backend shows debug borders on layers
        """


    @proxy_target_command
    async def setShowFPSCounter(self, show):
        """
            Requests that backend shows the FPS counter
        """


    @proxy_target_command
    async def setShowPaintRects(self, result):
        """
            Requests that backend shows paint rectangles
        """


    @proxy_target_command
    async def setShowScrollBottleneckRects(self, show):
        """
            Requests that backend shows scroll bottleneck rects
        """


    @proxy_target_command
    async def setShowHitTestBorders(self, show):
        """
            Requests that backend shows hit-test borders on layers
        """


    @proxy_target_command
    async def setShowViewportSizeOnResize(self, show):
        """
            Paints viewport size upon main frame resize.
        """


    @proxy_target_command
    async def setSuspended(self, suspended):
        """
            None
        """

