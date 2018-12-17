from .decorators import proxy_target_command



class Audits(object):

    def __init__(self, devtools):
        self.devtools = devtools


    @proxy_target_command
    async def getEncodedResponse(self, requestId, encoding, quality=None, sizeOnly=None):
        """
            Returns the response body and size if it were re-encoded with the specified settings. Only
applies to images.
        """

