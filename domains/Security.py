from .decorators import proxy_target_command



class Security(object):

    def __init__(self, devtools):
        self.devtools = devtools


    @proxy_target_command
    async def disable(self):
        """
            Disables tracking security state changes.
        """


    @proxy_target_command
    async def enable(self):
        """
            Enables tracking security state changes.
        """


    @proxy_target_command
    async def setIgnoreCertificateErrors(self, ignore):
        """
            Enable/disable whether all certificate errors should be ignored.
        """


    @proxy_target_command
    async def handleCertificateError(self, eventId, action):
        """
            Handles a certificate error that fired a certificateError event.
        """


    @proxy_target_command
    async def setOverrideCertificateErrors(self, override):
        """
            Enable/disable overriding certificate errors. If enabled, all certificate error events need to
be handled by the DevTools client and should be answered with `handleCertificateError` commands.
        """

