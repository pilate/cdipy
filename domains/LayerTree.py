from .decorators import proxy_target_command



class LayerTree(object):

    def __init__(self, devtools):
        self.devtools = devtools


    @proxy_target_command
    async def compositingReasons(self, layerId):
        """
            Provides the reasons why the given layer was composited.
        """


    @proxy_target_command
    async def disable(self):
        """
            Disables compositing tree inspection.
        """


    @proxy_target_command
    async def enable(self):
        """
            Enables compositing tree inspection.
        """


    @proxy_target_command
    async def loadSnapshot(self, tiles):
        """
            Returns the snapshot identifier.
        """


    @proxy_target_command
    async def makeSnapshot(self, layerId):
        """
            Returns the layer snapshot identifier.
        """


    @proxy_target_command
    async def profileSnapshot(self, snapshotId, minRepeatCount=None, minDuration=None, clipRect=None):
        """
            None
        """


    @proxy_target_command
    async def releaseSnapshot(self, snapshotId):
        """
            Releases layer snapshot captured by the back-end.
        """


    @proxy_target_command
    async def replaySnapshot(self, snapshotId, fromStep=None, toStep=None, scale=None):
        """
            Replays the layer snapshot and returns the resulting bitmap.
        """


    @proxy_target_command
    async def snapshotCommandLog(self, snapshotId):
        """
            Replays the layer snapshot and returns canvas log.
        """

