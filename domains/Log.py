from .decorators import proxy_target_command



class Log(object):

    def __init__(self, devtools):
        self.devtools = devtools


    @proxy_target_command
    async def clear(self):
        """
            Clears the log.
        """


    @proxy_target_command
    async def disable(self):
        """
            Disables log domain, prevents further log entries from being reported to the client.
        """


    @proxy_target_command
    async def enable(self):
        """
            Enables log domain, sends the entries collected so far to the client by means of the
`entryAdded` notification.
        """


    @proxy_target_command
    async def startViolationsReport(self, config):
        """
            start violation reporting.
        """


    @proxy_target_command
    async def stopViolationsReport(self):
        """
            Stop violation reporting.
        """

