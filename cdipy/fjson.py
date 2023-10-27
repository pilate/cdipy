# Try JSON libraries in descending order of performance

try:
    from orjson import dumps as _dumps
    from orjson import loads

    # orjson returns bytes
    def dumps(data):
        return _dumps(data).decode("utf-8")

except ModuleNotFoundError:
    try:
        from ujson import dumps, loads
    except ModuleNotFoundError:
        from json import dumps, loads


__all__ = ["dumps", "loads"]
