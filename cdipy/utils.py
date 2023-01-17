import asyncio
import logging
import os

import aiohttp


DL_ROOT = "https://raw.githubusercontent.com/ChromeDevTools/devtools-protocol/master/json"
SOURCE_FILES = [
    f"{DL_ROOT}/browser_protocol.json",
    f"{DL_ROOT}/js_protocol.json"
]

LOGGER = logging.getLogger("cdipy.utils")

def get_cache_path():
    cache_dir = os.environ.get("CDIPY_CACHE")
    if cache_dir:
        return cache_dir

    xdg_cache_home = os.getenv("XDG_CACHE_HOME")
    if not xdg_cache_home:
        user_home = os.getenv("HOME")
        if user_home:
            xdg_cache_home = os.path.join(user_home, ".cache")

    if xdg_cache_home:
        return os.path.join(xdg_cache_home, "python-cdipy")

    return os.path.join(os.path.dirname(__file__), ".cache")


async def download_data():
    async with aiohttp.ClientSession() as session:
        requests = []
        for url in SOURCE_FILES:
            LOGGER.debug("Downloading %s", url)
            requests.append(session.get(url))

        responses = await asyncio.gather(*requests)
        for response in responses:
            new_path = get_cache_path() / response.url.name
            with open(new_path, "w+b") as f:
                f.write(await response.read())
            LOGGER.debug("Wrote %s", new_path)
