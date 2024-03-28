from random import choices
import string


def create_random_string(num=6):
    return ''.join(choices(string.ascii_lowercase + string.digits, k=num))