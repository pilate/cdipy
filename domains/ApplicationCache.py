from .decorators import proxy_target_command



class ApplicationCache(object):

    def __init__(self, devtools):
        self.devtools = devtools


    @proxy_target_command
    async def enable(self):
        """
            Enables application cache domain notifications.
        """


    @proxy_target_command
    async def getApplicationCacheForFrame(self, frameId):
        """
            Returns relevant application cache data for the document in given frame.
        """


    @proxy_target_command
    async def getFramesWithManifests(self):
        """
            Returns array of frame identifiers with manifest urls for each frame containing a document
associated with some application cache.
        """


    @proxy_target_command
    async def getManifestForFrame(self, frameId):
        """
            Returns manifest URL for document in the given frame.
        """

