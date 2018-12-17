from .decorators import proxy_target_command



class Inspector(object):

    def __init__(self, devtools):
        self.devtools = devtools


    @proxy_target_command
    async def disable(self):
        """
            Disables inspector domain notifications.
        """


    @proxy_target_command
    async def enable(self):
        """
            Enables inspector domain notifications.
        """

