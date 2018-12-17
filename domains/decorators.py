from functools import wraps

import inspect


# defaults = argspec.defaults
# for offset, default in enumerate(defaults, -len(defaults)):
#     arg = argspec.args[offset]
#     if arg not in kwargs:
#         kwargs[arg] = default


def proxy_command(fn):
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

        command = ".".join([self.__class__.__name__, fn.__name__])
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