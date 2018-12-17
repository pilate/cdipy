from .decorators import proxy_target_command



class Animation(object):

    def __init__(self, devtools):
        self.devtools = devtools


    @proxy_target_command
    async def disable(self):
        """
            Disables animation domain notifications.
        """


    @proxy_target_command
    async def enable(self):
        """
            Enables animation domain notifications.
        """


    @proxy_target_command
    async def getCurrentTime(self, id):
        """
            Returns the current time of the an animation.
        """


    @proxy_target_command
    async def getPlaybackRate(self):
        """
            Gets the playback rate of the document timeline.
        """


    @proxy_target_command
    async def releaseAnimations(self, animations):
        """
            Releases a set of animations to no longer be manipulated.
        """


    @proxy_target_command
    async def resolveAnimation(self, animationId):
        """
            Gets the remote object of the Animation.
        """


    @proxy_target_command
    async def seekAnimations(self, animations, currentTime):
        """
            Seek a set of animations to a particular time within each animation.
        """


    @proxy_target_command
    async def setPaused(self, animations, paused):
        """
            Sets the paused state of a set of animations.
        """


    @proxy_target_command
    async def setPlaybackRate(self, playbackRate):
        """
            Sets the playback rate of the document timeline.
        """


    @proxy_target_command
    async def setTiming(self, animationId, duration, delay):
        """
            Sets the timing of an animation node.
        """

