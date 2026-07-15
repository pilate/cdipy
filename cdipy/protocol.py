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


class DynamicDomain:
    """
    Resolves commands by name, for when validation (and the protocol
    download) is skipped. cdi.Page.navigate(...) -> execute_method("Page.navigate", ...)
    """

    def __init__(self, devtools, name):
        self.devtools = devtools
        self.name = name
        self.commands = {}

    def __getattr__(self, command_name):
        if wrapper := self.commands.get(command_name):
            return wrapper

        if command_name.startswith("_"):
            raise AttributeError(command_name)

        command_str = f"{self.name}.{command_name}"

        async def wrapper(**kwargs):
            wait = kwargs.pop("_wait", True)
            return await self.devtools.execute_method(command_str, kwargs, wait=wait)

        self.commands[command_name] = wrapper
        return wrapper


class DynamicDomains:
    """DOMAINS stand-in: any capitalized name resolves to a domain."""

    @staticmethod
    def get(name):
        if name[:1].isupper():
            return lambda devtools: DynamicDomain(devtools, name)


def load_domains():
    cache_path = get_cache_path()

    if not os.path.exists(cache_path):
        os.makedirs(cache_path, mode=0o755)

    if not any(name.endswith(".json") for name in os.listdir(cache_path)):
        update_protocol_data()

    domains = {}
    for filename in os.listdir(cache_path):
        if not filename.endswith(".json"):
            continue

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


DOMAINS = DynamicDomains() if SKIP_VALIDATION else load_domains()
