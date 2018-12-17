from .decorators import proxy_target_command



class Testing(object):

    def __init__(self, devtools):
        self.devtools = devtools


    @proxy_target_command
    async def generateTestReport(self, message, group=None):
        """
            Generates a report for testing.
        """

