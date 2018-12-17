from .decorators import proxy_target_command



class DeviceOrientation(object):

    def __init__(self, devtools):
        self.devtools = devtools


    @proxy_target_command
    async def clearDeviceOrientationOverride(self):
        """
            Clears the overridden Device Orientation.
        """


    @proxy_target_command
    async def setDeviceOrientationOverride(self, alpha, beta, gamma):
        """
            Overrides the Device Orientation.
        """

