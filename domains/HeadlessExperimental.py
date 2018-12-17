from .decorators import proxy_target_command



class HeadlessExperimental(object):

    def __init__(self, devtools):
        self.devtools = devtools


    @proxy_target_command
    async def beginFrame(self, frameTimeTicks=None, interval=None, noDisplayUpdates=None, screenshot=None):
        """
            Sends a BeginFrame to the target and returns when the frame was completed. Optionally captures a
screenshot from the resulting frame. Requires that the target was created with enabled
BeginFrameControl. Designed for use with --run-all-compositor-stages-before-draw, see also
https://goo.gl/3zHXhB for more background.
        """


    @proxy_target_command
    async def disable(self):
        """
            Disables headless events for the target.
        """


    @proxy_target_command
    async def enable(self):
        """
            Enables headless events for the target.
        """

