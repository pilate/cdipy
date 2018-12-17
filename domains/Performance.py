from .decorators import proxy_target_command



class Performance(object):

    def __init__(self, devtools):
        self.devtools = devtools


    @proxy_target_command
    async def disable(self):
        """
            Disable collecting and reporting metrics.
        """


    @proxy_target_command
    async def enable(self):
        """
            Enable collecting and reporting metrics.
        """


    @proxy_target_command
    async def setTimeDomain(self, timeDomain):
        """
            Sets time domain to use for collecting and reporting duration metrics.
Note that this must be called before enabling metrics collection. Calling
this method while metrics collection is enabled returns an error.
        """


    @proxy_target_command
    async def getMetrics(self):
        """
            Retrieve current values of run-time metrics.
        """

