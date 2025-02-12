import asyncio
import logging
import os
from pathlib import Path

import aiohttp


LOGGER = logging.getLogger("cdipy.utils")

ROOT = "https://raw.githubusercontent.com/ChromeDevTools/devtools-protocol/master/json"
SOURCE_FILES = [f"{ROOT}/browser_protocol.json", f"{ROOT}/js_protocol.json"]
OS_VAR = "CDIPY_CACHE"


def get_cache_path() -> Path:
    """
    Search system paths for existing cache
    """
    cache_dir = os.environ.get(OS_VAR)
    if cache_dir:
        return Path(cache_dir)

    xdg_cache_home = os.getenv("XDG_CACHE_HOME")
    if not xdg_cache_home:
        if user_home := os.getenv("HOME"):
            xdg_cache_home = os.path.join(user_home, ".cache")

    if xdg_cache_home:
        full_path = os.path.join(xdg_cache_home, "python-cdipy")
    else:
        full_path = os.path.join(os.path.dirname(__file__), ".cache")

    os.environ[OS_VAR] = full_path
    return Path(full_path)


async def update_protocol_data() -> None:
    """
    Download latest protocol definition
    """
    async with aiohttp.ClientSession() as session:
        requests = []
        for url in SOURCE_FILES:
            LOGGER.warning("Downloading %s", url)
            requests.append(session.get(url))

        responses = await asyncio.gather(*requests)
        for response in responses:
            new_path = get_cache_path() / response.url.name
            with open(new_path, "w+b") as fp:
                fp.write(await response.read())
            LOGGER.warning("Wrote %s", new_path)
