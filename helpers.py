import asyncio


def async_wrapper(sync_fn):
    def inner(*args):
        return asyncio.get_running_loop().run_in_executor(None, sync_fn, *args)
    return inner
