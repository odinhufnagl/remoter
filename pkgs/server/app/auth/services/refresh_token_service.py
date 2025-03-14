import jwt
from pydantic import BaseModel
from app.auth.services.jwt_token_service import JwtTokenService, Payload
from app.config import settings
from app.shared.core.errors.result_errors.token_errors import TokenErrors
from app.shared.core.result.result import Result


class RefreshTokenPayload(BaseModel):
    user_id: str


class RefreshTokenService(JwtTokenService[RefreshTokenPayload]):
    secret = settings.REFRESH_TOKEN_SECRET
    expirationTime = settings.REFRESH_TOKEN_EXPIRE_MINUTES

    @classmethod
    def parse_token(cls, token: str) -> Result[RefreshTokenPayload]:
        try:
            payload = jwt.decode(token, cls.secret, algorithms=[cls.algorithm])
            print("ppppp", payload)
            return Result.ok(RefreshTokenPayload(user_id=payload["user_id"]))
        except Exception as e:
            print("hahaeh", e)
            return Result.fail(TokenErrors.invalid_token())
