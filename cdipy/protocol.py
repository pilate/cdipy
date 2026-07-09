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


def add_command(domain_class, command):
    """
    Creates a new function that can be used as a domain method
    """
    command_name = command["name"]
    command_str = f"{domain_class.__name__}.{command_name}"

    parameters = command.get("parameters", [])
    valid_params = frozenset(param["name"] for param in parameters)
    required_params = frozenset(
        param["name"] for param in parameters if not param.get("optional")
    )

    if SKIP_VALIDATION:
        async def wrapper(self, **kwargs):
            wait = kwargs.pop("_wait", True)
            return await self.devtools.execute_method(command_str, kwargs, wait=wait)

    else:
        async def wrapper(self, **kwargs):
            wait = kwargs.pop("_wait", True)
            if missing := required_params - kwargs.keys():
                raise TypeError(
                    f"{command_str}() missing required arguments: {', '.join(sorted(missing))}"
                )
            if unexpected := kwargs.keys() - valid_params:
                raise TypeError(
                    f"{command_str}() got unexpected arguments: {', '.join(sorted(unexpected))}"
                )
            return await self.devtools.execute_method(command_str, kwargs, wait=wait)

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
