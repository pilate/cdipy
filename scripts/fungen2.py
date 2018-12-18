from functools import wraps
from types import MethodType

import asyncio
import inspect
import logging
import types

import requests

from chrome import ChromeDevTools




logger = logging.getLogger("cdipy.scripts.gen")
logger.setLevel(10)
logging.basicConfig(format="[%(asctime)s] [%(levelname)s] %(message)s")
 

SELF_PARAM = inspect.Parameter(name="self", kind=inspect.Parameter.POSITIONAL_OR_KEYWORD)


def proxy_command(fn):
    @wraps(fn)
    async def wrapper(*args, **kwargs):
        bound = fn._sig.bind(*args, **kwargs)
        kwargs = bound.arguments
        self = kwargs.pop("self")
        command = f"{self.__class__.__name__}.{fn.__name__}"
        return await self.devtools.run_command(command, **kwargs)

    return wrapper


def proxy_target_command(fn):
    argspec = inspect.getargspec(fn)

    @wraps(fn)
    async def wrapper(*args, **kwargs):
        self = args[0]

        # Make all args kwargs
        for offset, arg in enumerate(args):
            arg_name = argspec.args[offset]
            if arg_name == "self":
                continue
            kwargs[arg_name] = arg

        kwargs["sessionId"] = kwargs.get("sessionId", self.devtools.attached_session)

        command = ".".join([self.__class__.__name__, fn.__name__])
        return await self.devtools.run_target_command(command, **kwargs)

    return wrapper


def create_signature(params):
    new_params = [SELF_PARAM]

    for param in params:
        default = inspect.Parameter.empty
        if param.get("optional"):
            default = None

        new_param = inspect.Parameter(
            name=param["name"], 
            kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
            default=default)

        new_params.append(new_param)   

    return inspect.Signature(parameters=new_params)


class DomainProxy(object):

    def __init__(self, devtools):
        self.devtools = devtools


    def add_command(self, command):

        def function(*args, **kwargs):
            pass

        function._sig = create_signature(command.get("parameters", []))
        function.__name__ = function.__qualname__ = command["name"]

        setattr(self, command["name"], MethodType(proxy_command(function), self))


async def main():
    protocol = requests.get("https://raw.githubusercontent.com/ChromeDevTools/devtools-protocol/master/json/browser_protocol.json").json()

    logger.debug("Generating objects for protocol version {0}.{1}".format(
        protocol["version"]["major"], protocol["version"]["minor"]))

    cdt = ChromeDevTools()
    await cdt.launch()

    for domain in protocol["domains"]:
        domain_class = types.new_class(domain["domain"], (DomainProxy, ))
        blank = domain_class(cdt)
        for command in domain.get("commands", []):
            blank.add_command(command)
            
        setattr(cdt, domain["domain"], blank)

    target = await cdt.Target.createTarget("about:blank")
    session = await cdt.Target.attachToTarget(targetId=target["targetId"])
    await cdt.Page.enable()
    await cdt.Network.enable()
    await cdt.Target.detachFromTarget(**session)





asyncio.get_event_loop().run_until_complete(main())
