import datetime
import random
import string


def random_string(string_length=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))


def from_date_to_str(date: datetime) -> str:
    return date.strftime("%d-%b-%Y %H:%M:%S.%f")