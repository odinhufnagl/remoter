from typing import Optional


_api_key: Optional[str] = None


def set_api_key(api_key: str) -> None:
    global _api_key
    _api_key = api_key


def get_api_key() -> Optional[str]:
    global _api_key
    return _api_key
