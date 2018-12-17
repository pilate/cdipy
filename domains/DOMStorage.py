from .decorators import proxy_target_command



class DOMStorage(object):

    def __init__(self, devtools):
        self.devtools = devtools


    @proxy_target_command
    async def clear(self, storageId):
        """
            None
        """


    @proxy_target_command
    async def disable(self):
        """
            Disables storage tracking, prevents storage events from being sent to the client.
        """


    @proxy_target_command
    async def enable(self):
        """
            Enables storage tracking, storage events will now be delivered to the client.
        """


    @proxy_target_command
    async def getDOMStorageItems(self, storageId):
        """
            None
        """


    @proxy_target_command
    async def removeDOMStorageItem(self, storageId, key):
        """
            None
        """


    @proxy_target_command
    async def setDOMStorageItem(self, storageId, key, value):
        """
            None
        """

