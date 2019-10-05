import asyncio
import datetime
import random
import string


def async_wrapper(sync_fn):
    def inner(*args):
        return asyncio.get_running_loop().run_in_executor(None, sync_fn, *args)
    return inner


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def from_date_to_str(date: datetime) -> str:
    return date.strftime("%d-%b-%Y %H:%M:%S.%f")