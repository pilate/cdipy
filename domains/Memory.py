from .decorators import proxy_target_command



class Memory(object):

    def __init__(self, devtools):
        self.devtools = devtools


    @proxy_target_command
    async def getDOMCounters(self):
        """
            None
        """


    @proxy_target_command
    async def prepareForLeakDetection(self):
        """
            None
        """


    @proxy_target_command
    async def setPressureNotificationsSuppressed(self, suppressed):
        """
            Enable/disable suppressing memory pressure notifications in all processes.
        """


    @proxy_target_command
    async def simulatePressureNotification(self, level):
        """
            Simulate a memory pressure notification in all processes.
        """


    @proxy_target_command
    async def startSampling(self, samplingInterval=None, suppressRandomness=None):
        """
            Start collecting native memory profile.
        """


    @proxy_target_command
    async def stopSampling(self):
        """
            Stop collecting native memory profile.
        """


    @proxy_target_command
    async def getAllTimeSamplingProfile(self):
        """
            Retrieve native memory allocations profile
collected since renderer process startup.
        """


    @proxy_target_command
    async def getBrowserSamplingProfile(self):
        """
            Retrieve native memory allocations profile
collected since browser process startup.
        """


    @proxy_target_command
    async def getSamplingProfile(self):
        """
            Retrieve native memory allocations profile collected since last
`startSampling` call.
        """

