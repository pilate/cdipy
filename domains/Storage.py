from .decorators import proxy_target_command



class Storage(object):

    def __init__(self, devtools):
        self.devtools = devtools


    @proxy_target_command
    async def clearDataForOrigin(self, origin, storageTypes):
        """
            Clears storage for origin.
        """


    @proxy_target_command
    async def getUsageAndQuota(self, origin):
        """
            Returns usage and quota in bytes.
        """


    @proxy_target_command
    async def trackCacheStorageForOrigin(self, origin):
        """
            Registers origin to be notified when an update occurs to its cache storage list.
        """


    @proxy_target_command
    async def trackIndexedDBForOrigin(self, origin):
        """
            Registers origin to be notified when an update occurs to its IndexedDB.
        """


    @proxy_target_command
    async def untrackCacheStorageForOrigin(self, origin):
        """
            Unregisters origin from receiving notifications for cache storage.
        """


    @proxy_target_command
    async def untrackIndexedDBForOrigin(self, origin):
        """
            Unregisters origin from receiving notifications for IndexedDB.
        """

