import jwt
from pydantic import BaseModel
from app.auth.services.jwt_token_service import JwtTokenService
from app.config import settings
from app.shared.core.errors.result_errors.token_errors import TokenError, TokenErrors
from app.shared.core.result.result import Result


class AccessTokenPayload(BaseModel):
    user_id: str


class AccessTokenService(JwtTokenService[AccessTokenPayload]):
    secret = settings.ACCESS_TOKEN_SECRET
    expirationTime = settings.ACCESS_TOKEN_EXPIRE_MINUTES

    @classmethod
    def parse_token(cls, token: str) -> Result[AccessTokenPayload]:
        try:
            payload = jwt.decode(token, cls.secret, algorithms=[cls.algorithm])
            return Result.ok(AccessTokenPayload(user_id=payload["user_id"]))
        except Exception as e:
            print("eehahah", e)
            return Result.fail(TokenErrors.invalid_token())
