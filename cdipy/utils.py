import logging
import os
import urllib.request
from pathlib import Path


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


def update_protocol_data() -> None:
    """
    Download latest protocol definition
    """
    for url in SOURCE_FILES:
        LOGGER.warning("Downloading %s", url)
        with urllib.request.urlopen(url) as response:
            data = response.read()

        new_path = get_cache_path() / url.rsplit("/", 1)[1]

        # Write to a temp name and rename so a partial download can never
        # be mistaken for a valid cache file
        tmp_path = new_path.with_suffix(".tmp")
        tmp_path.write_bytes(data)
        tmp_path.replace(new_path)
        LOGGER.warning("Wrote %s", new_path)
