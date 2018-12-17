from .decorators import proxy_target_command



class SystemInfo(object):

    def __init__(self, devtools):
        self.devtools = devtools


    @proxy_target_command
    async def getInfo(self):
        """
            Returns information about the system.
        """


    @proxy_target_command
    async def getProcessInfo(self):
        """
            Returns information about all running processes.
        """

