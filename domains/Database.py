from .decorators import proxy_target_command



class Database(object):

    def __init__(self, devtools):
        self.devtools = devtools


    @proxy_target_command
    async def disable(self):
        """
            Disables database tracking, prevents database events from being sent to the client.
        """


    @proxy_target_command
    async def enable(self):
        """
            Enables database tracking, database events will now be delivered to the client.
        """


    @proxy_target_command
    async def executeSQL(self, databaseId, query):
        """
            None
        """


    @proxy_target_command
    async def getDatabaseTableNames(self, databaseId):
        """
            None
        """

