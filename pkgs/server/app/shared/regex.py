import re


def regex_email(address) -> bool:
    return re.match(r"^\S+@\S+\.\S+$", address) is not None
