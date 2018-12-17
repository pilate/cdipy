from .decorators import proxy_target_command



class CacheStorage(object):

    def __init__(self, devtools):
        self.devtools = devtools


    @proxy_target_command
    async def deleteCache(self, cacheId):
        """
            Deletes a cache.
        """


    @proxy_target_command
    async def deleteEntry(self, cacheId, request):
        """
            Deletes a cache entry.
        """


    @proxy_target_command
    async def requestCacheNames(self, securityOrigin):
        """
            Requests cache names.
        """


    @proxy_target_command
    async def requestCachedResponse(self, cacheId, requestURL):
        """
            Fetches cache entry.
        """


    @proxy_target_command
    async def requestEntries(self, cacheId, skipCount, pageSize, pathFilter=None):
        """
            Requests data from cache.
        """

