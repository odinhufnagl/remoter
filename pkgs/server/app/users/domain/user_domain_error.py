from app.shared.core.result.result_error import ResultError


UserDomainCodes = {
    "EMAIL_NOT_VALID": 400,
}


class UserDomainError(ResultError):
    @staticmethod
    def email_not_valid() -> "UserDomainError":
        return UserDomainError(
            code=UserDomainCodes["EMAIL_NOT_VALID"], message="Email is not valid"
        )
