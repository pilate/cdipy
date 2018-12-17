from .decorators import proxy_target_command



class IO(object):

    def __init__(self, devtools):
        self.devtools = devtools


    @proxy_target_command
    async def close(self, handle):
        """
            Close the stream, discard any temporary backing storage.
        """


    @proxy_target_command
    async def read(self, handle, offset=None, size=None):
        """
            Read a chunk of the stream
        """


    @proxy_target_command
    async def resolveBlob(self, objectId):
        """
            Return UUID of Blob object specified by a remote object id.
        """

