from os import stat
from app.shared.core.result.result_error import ResultError

API_KEY_ERROR_CODES = {
    "INVALID_KEY": 6100,
    "KEY_NOT_FOUND": 6101,
    "KEY_NOT_CORRECT": 6102,
}


class ApiKeyError(ResultError):
    codes: dict = API_KEY_ERROR_CODES


class ApiKeyErrors:
    @staticmethod
    def invalid_key() -> "ApiKeyError":
        return ApiKeyError(
            code=API_KEY_ERROR_CODES["INVALID_KEY"], message="Invalid key"
        )

    @staticmethod
    def key_not_found() -> "ApiKeyError":
        return ApiKeyError(
            code=API_KEY_ERROR_CODES["KEY_NOT_FOUND"], message="Key not found"
        )

    @staticmethod
    def key_not_correct() -> "ApiKeyError":
        return ApiKeyError(
            code=API_KEY_ERROR_CODES["KEY_NOT_CORRECT"], message="Key not correct"
        )
