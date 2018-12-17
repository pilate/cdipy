from .decorators import proxy_target_command



class DOM(object):

    def __init__(self, devtools):
        self.devtools = devtools


    @proxy_target_command
    async def collectClassNamesFromSubtree(self, nodeId):
        """
            Collects class names for the node with given id and all of it's child nodes.
        """


    @proxy_target_command
    async def copyTo(self, nodeId, targetNodeId, insertBeforeNodeId=None):
        """
            Creates a deep copy of the specified node and places it into the target container before the
given anchor.
        """


    @proxy_target_command
    async def describeNode(self, nodeId=None, backendNodeId=None, objectId=None, depth=None, pierce=None):
        """
            Describes node given its id, does not require domain to be enabled. Does not start tracking any
objects, can be used for automation.
        """


    @proxy_target_command
    async def disable(self):
        """
            Disables DOM agent for the given page.
        """


    @proxy_target_command
    async def discardSearchResults(self, searchId):
        """
            Discards search results from the session with the given id. `getSearchResults` should no longer
be called for that search.
        """


    @proxy_target_command
    async def enable(self):
        """
            Enables DOM agent for the given page.
        """


    @proxy_target_command
    async def focus(self, nodeId=None, backendNodeId=None, objectId=None):
        """
            Focuses the given element.
        """


    @proxy_target_command
    async def getAttributes(self, nodeId):
        """
            Returns attributes for the specified node.
        """


    @proxy_target_command
    async def getBoxModel(self, nodeId=None, backendNodeId=None, objectId=None):
        """
            Returns boxes for the given node.
        """


    @proxy_target_command
    async def getContentQuads(self, nodeId=None, backendNodeId=None, objectId=None):
        """
            Returns quads that describe node position on the page. This method
might return multiple quads for inline nodes.
        """


    @proxy_target_command
    async def getDocument(self, depth=None, pierce=None):
        """
            Returns the root DOM node (and optionally the subtree) to the caller.
        """


    @proxy_target_command
    async def getFlattenedDocument(self, depth=None, pierce=None):
        """
            Returns the root DOM node (and optionally the subtree) to the caller.
        """


    @proxy_target_command
    async def getNodeForLocation(self, x, y, includeUserAgentShadowDOM=None):
        """
            Returns node id at given location. Depending on whether DOM domain is enabled, nodeId is
either returned or not.
        """


    @proxy_target_command
    async def getOuterHTML(self, nodeId=None, backendNodeId=None, objectId=None):
        """
            Returns node's HTML markup.
        """


    @proxy_target_command
    async def getRelayoutBoundary(self, nodeId):
        """
            Returns the id of the nearest ancestor that is a relayout boundary.
        """


    @proxy_target_command
    async def getSearchResults(self, searchId, fromIndex, toIndex):
        """
            Returns search results from given `fromIndex` to given `toIndex` from the search with the given
identifier.
        """


    @proxy_target_command
    async def hideHighlight(self):
        """
            Hides any highlight.
        """


    @proxy_target_command
    async def highlightNode(self):
        """
            Highlights DOM node.
        """


    @proxy_target_command
    async def highlightRect(self):
        """
            Highlights given rectangle.
        """


    @proxy_target_command
    async def markUndoableState(self):
        """
            Marks last undoable state.
        """


    @proxy_target_command
    async def moveTo(self, nodeId, targetNodeId, insertBeforeNodeId=None):
        """
            Moves node into the new container, places it before the given anchor.
        """


    @proxy_target_command
    async def performSearch(self, query, includeUserAgentShadowDOM=None):
        """
            Searches for a given string in the DOM tree. Use `getSearchResults` to access search results or
`cancelSearch` to end this search session.
        """


    @proxy_target_command
    async def pushNodeByPathToFrontend(self, path):
        """
            Requests that the node is sent to the caller given its path. // FIXME, use XPath
        """


    @proxy_target_command
    async def pushNodesByBackendIdsToFrontend(self, backendNodeIds):
        """
            Requests that a batch of nodes is sent to the caller given their backend node ids.
        """


    @proxy_target_command
    async def querySelector(self, nodeId, selector):
        """
            Executes `querySelector` on a given node.
        """


    @proxy_target_command
    async def querySelectorAll(self, nodeId, selector):
        """
            Executes `querySelectorAll` on a given node.
        """


    @proxy_target_command
    async def redo(self):
        """
            Re-does the last undone action.
        """


    @proxy_target_command
    async def removeAttribute(self, nodeId, name):
        """
            Removes attribute with given name from an element with given id.
        """


    @proxy_target_command
    async def removeNode(self, nodeId):
        """
            Removes node with given id.
        """


    @proxy_target_command
    async def requestChildNodes(self, nodeId, depth=None, pierce=None):
        """
            Requests that children of the node with given id are returned to the caller in form of
`setChildNodes` events where not only immediate children are retrieved, but all children down to
the specified depth.
        """


    @proxy_target_command
    async def requestNode(self, objectId):
        """
            Requests that the node is sent to the caller given the JavaScript node object reference. All
nodes that form the path from the node to the root are also sent to the client as a series of
`setChildNodes` notifications.
        """


    @proxy_target_command
    async def resolveNode(self, nodeId=None, backendNodeId=None, objectGroup=None):
        """
            Resolves the JavaScript node object for a given NodeId or BackendNodeId.
        """


    @proxy_target_command
    async def setAttributeValue(self, nodeId, name, value):
        """
            Sets attribute for an element with given id.
        """


    @proxy_target_command
    async def setAttributesAsText(self, nodeId, text, name=None):
        """
            Sets attributes on element with given id. This method is useful when user edits some existing
attribute value and types in several attribute name/value pairs.
        """


    @proxy_target_command
    async def setFileInputFiles(self, files, nodeId=None, backendNodeId=None, objectId=None):
        """
            Sets files for the given file input element.
        """


    @proxy_target_command
    async def getFileInfo(self, objectId):
        """
            Returns file information for the given
File wrapper.
        """


    @proxy_target_command
    async def setInspectedNode(self, nodeId):
        """
            Enables console to refer to the node with given id via $x (see Command Line API for more details
$x functions).
        """


    @proxy_target_command
    async def setNodeName(self, nodeId, name):
        """
            Sets node name for a node with given id.
        """


    @proxy_target_command
    async def setNodeValue(self, nodeId, value):
        """
            Sets node value for a node with given id.
        """


    @proxy_target_command
    async def setOuterHTML(self, nodeId, outerHTML):
        """
            Sets node HTML markup, returns new node id.
        """


    @proxy_target_command
    async def undo(self):
        """
            Undoes the last performed action.
        """


    @proxy_target_command
    async def getFrameOwner(self, frameId):
        """
            Returns iframe node that owns iframe with the given domain.
        """

