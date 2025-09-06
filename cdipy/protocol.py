import asyncio
import inspect
import os
import types

import msgspec.json

from .utils import get_cache_path, update_protocol_data


SKIP_VALIDATION = os.environ.get("CDIPY_SKIP_VALIDATION", False)


class DomainBase:  # pylint: disable=too-few-public-methods
    """
    Template class used for domains (ex: obj.Page)
    """

    __slots__ = ("devtools",)

    def __init__(self, devtools):
        self.devtools = devtools


def params_to_signature(params):
    """
    Creates a function signature based on a list of protocol parameters
    """
    new_params = []

    for param in params:
        default = inspect.Parameter.empty
        if param.get("optional"):
            default = None

        new_param = inspect.Parameter(
            name=param["name"],
            kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
            default=default,
        )

        new_params.append(new_param)

    new_params.sort(key=lambda p: bool(p.default), reverse=True)

    return inspect.Signature(parameters=new_params)


def add_command(domain_class, command):
    """
    Creates a new function that can be used as a domain method
    """
    command_name = command["name"]
    command_str = f"{domain_class.__name__}.{command_name}"

    signature = params_to_signature(command.get("parameters", []))

    async def wrapper(self, **kwargs):
        """
        Validate method arguments against `signature`
        Pass validated args to execute_method
        """
        if not SKIP_VALIDATION:
            kwargs = signature.bind(**kwargs).arguments

        return await self.devtools.execute_method(command_str, **kwargs)

    wrapper.__name__ = wrapper.__qualname__ = command_str

    setattr(domain_class, command_name, wrapper)


def load_domains():
    cache_path = get_cache_path()

    if not os.path.exists(cache_path):
        os.makedirs(cache_path, mode=0o744)

    if not os.listdir(cache_path):
        asyncio.get_event_loop().run_until_complete(update_protocol_data())

    domains = {}
    for filename in os.listdir(cache_path):
        with open(cache_path / filename, "rb") as fp:
            data = msgspec.json.decode(fp.read())

        for domain in data.get("domains", []):
            domain_name = domain["domain"]

            # Create a new class for each domain
            domain_class = types.new_class(domain_name, (DomainBase,))

            # Add each command to the domain class
            for command in domain.get("commands", []):
                add_command(domain_class, command)

            domains[domain_name] = domain_class

    return domains


DOMAINS = load_domains()
