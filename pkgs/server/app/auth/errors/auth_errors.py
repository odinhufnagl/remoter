from app.shared.core.result.result_error import ResultError


from app.shared.core.result.result_error import ResultError

AUTH_ERROR_CODES = {
    "LOGIN_FAIL": 7000,
    "INVALID_CREDENTIALS": 7001,
}


class AuthError(ResultError):
    codes: dict = AUTH_ERROR_CODES


class AuthErrors:
    @staticmethod
    def login_fail() -> "AuthError":
        return AuthError(
            code=AUTH_ERROR_CODES["LOGIN_FAIL"],
            message="Incorrect username or password",
        )

    @staticmethod
    def invalid_credentials() -> "AuthError":
        return AuthError(
            code=AUTH_ERROR_CODES["INVALID_CREDENTIALS"],
            message="Invalid credentials",
        )
