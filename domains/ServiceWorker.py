from .decorators import proxy_target_command



class ServiceWorker(object):

    def __init__(self, devtools):
        self.devtools = devtools


    @proxy_target_command
    async def deliverPushMessage(self, origin, registrationId, data):
        """
            None
        """


    @proxy_target_command
    async def disable(self):
        """
            None
        """


    @proxy_target_command
    async def dispatchSyncEvent(self, origin, registrationId, tag, lastChance):
        """
            None
        """


    @proxy_target_command
    async def enable(self):
        """
            None
        """


    @proxy_target_command
    async def inspectWorker(self, versionId):
        """
            None
        """


    @proxy_target_command
    async def setForceUpdateOnPageLoad(self, forceUpdateOnPageLoad):
        """
            None
        """


    @proxy_target_command
    async def skipWaiting(self, scopeURL):
        """
            None
        """


    @proxy_target_command
    async def startWorker(self, scopeURL):
        """
            None
        """


    @proxy_target_command
    async def stopAllWorkers(self):
        """
            None
        """


    @proxy_target_command
    async def stopWorker(self, versionId):
        """
            None
        """


    @proxy_target_command
    async def unregister(self, scopeURL):
        """
            None
        """


    @proxy_target_command
    async def updateRegistration(self, scopeURL):
        """
            None
        """

