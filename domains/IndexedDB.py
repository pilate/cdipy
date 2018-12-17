from .decorators import proxy_target_command



class IndexedDB(object):

    def __init__(self, devtools):
        self.devtools = devtools


    @proxy_target_command
    async def clearObjectStore(self, securityOrigin, databaseName, objectStoreName):
        """
            Clears all entries from an object store.
        """


    @proxy_target_command
    async def deleteDatabase(self, securityOrigin, databaseName):
        """
            Deletes a database.
        """


    @proxy_target_command
    async def deleteObjectStoreEntries(self, securityOrigin, databaseName, objectStoreName, keyRange):
        """
            Delete a range of entries from an object store
        """


    @proxy_target_command
    async def disable(self):
        """
            Disables events from backend.
        """


    @proxy_target_command
    async def enable(self):
        """
            Enables events from backend.
        """


    @proxy_target_command
    async def requestData(self, securityOrigin, databaseName, objectStoreName, indexName, skipCount, pageSize, keyRange=None):
        """
            Requests data from object store or index.
        """


    @proxy_target_command
    async def requestDatabase(self, securityOrigin, databaseName):
        """
            Requests database with given name in given frame.
        """


    @proxy_target_command
    async def requestDatabaseNames(self, securityOrigin):
        """
            Requests database names for given security origin.
        """

