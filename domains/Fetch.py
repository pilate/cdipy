from .decorators import proxy_target_command



class Fetch(object):

    def __init__(self, devtools):
        self.devtools = devtools


    @proxy_target_command
    async def disable(self):
        """
            Disables the fetch domain.
        """


    @proxy_target_command
    async def enable(self, patterns=None, handleAuthRequests=None):
        """
            Enables issuing of requestPaused events. A request will be paused until client
calls one of failRequest, fulfillRequest or continueRequest/continueWithAuth.
        """


    @proxy_target_command
    async def failRequest(self, requestId, errorReason):
        """
            Causes the request to fail with specified reason.
        """


    @proxy_target_command
    async def fulfillRequest(self, requestId, responseCode, responseHeaders, body=None, responsePhrase=None):
        """
            Provides response to the request.
        """


    @proxy_target_command
    async def continueRequest(self, requestId, url=None, method=None, postData=None, headers=None):
        """
            Continues the request, optionally modifying some of its parameters.
        """


    @proxy_target_command
    async def continueWithAuth(self, requestId, authChallengeResponse):
        """
            Continues a request supplying authChallengeResponse following authRequired event.
        """


    @proxy_target_command
    async def getResponseBody(self, requestId):
        """
            Causes the body of the response to be received from the server and
returned as a single string. May only be issued for a request that
is paused in the Response stage and is mutually exclusive with
takeResponseBodyForInterceptionAsStream. Calling other methods that
affect the request or disabling fetch domain before body is received
results in an undefined behavior.
        """


    @proxy_target_command
    async def takeResponseBodyAsStream(self, requestId):
        """
            Returns a handle to the stream representing the response body.
The request must be paused in the HeadersReceived stage.
Note that after this command the request can't be continued
as is -- client either needs to cancel it or to provide the
response body.
The stream only supports sequential read, IO.read will fail if the position
is specified.
This method is mutually exclusive with getResponseBody.
Calling other methods that affect the request or disabling fetch
domain before body is received results in an undefined behavior.
        """

