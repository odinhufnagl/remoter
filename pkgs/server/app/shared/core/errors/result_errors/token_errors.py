from os import stat
from app.shared.core.result.result_error import ResultError

TOKEN_ERROR_CODES = {
    "INVALID_TOKEN": 6000,
    "TOKEN_NOT_FOUND": 6001,
    "TOKEN_NOT_CORRECT": 6002,
}


class TokenError(ResultError):
    codes: dict = TOKEN_ERROR_CODES


class TokenErrors:
    @staticmethod
    def invalid_token() -> "TokenError":
        return TokenError(
            code=TOKEN_ERROR_CODES["INVALID_TOKEN"], message="Invalid token"
        )

    @staticmethod
    def token_not_found() -> "TokenError":
        return TokenError(
            code=TOKEN_ERROR_CODES["TOKEN_NOT_FOUND"], message="Token not found"
        )

    @staticmethod
    def token_not_correct() -> "TokenError":
        return TokenError(
            code=TOKEN_ERROR_CODES["TOKEN_NOT_CORRECT"], message="Token not correct"
        )
