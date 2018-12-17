from .decorators import proxy_target_command



class Tethering(object):

    def __init__(self, devtools):
        self.devtools = devtools


    @proxy_target_command
    async def bind(self, port):
        """
            Request browser port binding.
        """


    @proxy_target_command
    async def unbind(self, port):
        """
            Request browser port unbinding.
        """

