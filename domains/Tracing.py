from .decorators import proxy_target_command



class Tracing(object):

    def __init__(self, devtools):
        self.devtools = devtools


    @proxy_target_command
    async def end(self):
        """
            Stop trace events collection.
        """


    @proxy_target_command
    async def getCategories(self):
        """
            Gets supported tracing categories.
        """


    @proxy_target_command
    async def recordClockSyncMarker(self, syncId):
        """
            Record a clock sync marker in the trace.
        """


    @proxy_target_command
    async def requestMemoryDump(self):
        """
            Request a global memory dump.
        """


    @proxy_target_command
    async def start(self, categories=None, options=None, bufferUsageReportingInterval=None, transferMode=None, streamCompression=None, traceConfig=None):
        """
            Start trace events collection.
        """

