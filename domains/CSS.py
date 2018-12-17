from .decorators import proxy_target_command



class CSS(object):

    def __init__(self, devtools):
        self.devtools = devtools


    @proxy_target_command
    async def addRule(self, styleSheetId, ruleText, location):
        """
            Inserts a new rule with the given `ruleText` in a stylesheet with given `styleSheetId`, at the
position specified by `location`.
        """


    @proxy_target_command
    async def collectClassNames(self, styleSheetId):
        """
            Returns all class names from specified stylesheet.
        """


    @proxy_target_command
    async def createStyleSheet(self, frameId):
        """
            Creates a new special "via-inspector" stylesheet in the frame with given `frameId`.
        """


    @proxy_target_command
    async def disable(self):
        """
            Disables the CSS agent for the given page.
        """


    @proxy_target_command
    async def enable(self):
        """
            Enables the CSS agent for the given page. Clients should not assume that the CSS agent has been
enabled until the result of this command is received.
        """


    @proxy_target_command
    async def forcePseudoState(self, nodeId, forcedPseudoClasses):
        """
            Ensures that the given node will have specified pseudo-classes whenever its style is computed by
the browser.
        """


    @proxy_target_command
    async def getBackgroundColors(self, nodeId):
        """
            None
        """


    @proxy_target_command
    async def getComputedStyleForNode(self, nodeId):
        """
            Returns the computed style for a DOM node identified by `nodeId`.
        """


    @proxy_target_command
    async def getInlineStylesForNode(self, nodeId):
        """
            Returns the styles defined inline (explicitly in the "style" attribute and implicitly, using DOM
attributes) for a DOM node identified by `nodeId`.
        """


    @proxy_target_command
    async def getMatchedStylesForNode(self, nodeId):
        """
            Returns requested styles for a DOM node identified by `nodeId`.
        """


    @proxy_target_command
    async def getMediaQueries(self):
        """
            Returns all media queries parsed by the rendering engine.
        """


    @proxy_target_command
    async def getPlatformFontsForNode(self, nodeId):
        """
            Requests information about platform fonts which we used to render child TextNodes in the given
node.
        """


    @proxy_target_command
    async def getStyleSheetText(self, styleSheetId):
        """
            Returns the current textual content for a stylesheet.
        """


    @proxy_target_command
    async def setEffectivePropertyValueForNode(self, nodeId, propertyName, value):
        """
            Find a rule with the given active property for the given node and set the new value for this
property
        """


    @proxy_target_command
    async def setKeyframeKey(self, styleSheetId, range, keyText):
        """
            Modifies the keyframe rule key text.
        """


    @proxy_target_command
    async def setMediaText(self, styleSheetId, range, text):
        """
            Modifies the rule selector.
        """


    @proxy_target_command
    async def setRuleSelector(self, styleSheetId, range, selector):
        """
            Modifies the rule selector.
        """


    @proxy_target_command
    async def setStyleSheetText(self, styleSheetId, text):
        """
            Sets the new stylesheet text.
        """


    @proxy_target_command
    async def setStyleTexts(self, edits):
        """
            Applies specified style edits one after another in the given order.
        """


    @proxy_target_command
    async def startRuleUsageTracking(self):
        """
            Enables the selector recording.
        """


    @proxy_target_command
    async def stopRuleUsageTracking(self):
        """
            Stop tracking rule usage and return the list of rules that were used since last call to
`takeCoverageDelta` (or since start of coverage instrumentation)
        """


    @proxy_target_command
    async def takeCoverageDelta(self):
        """
            Obtain list of rules that became used since last call to this method (or since start of coverage
instrumentation)
        """

