from abc import abstractmethod
from datetime import datetime, timedelta, timezone
from typing import Generic, TypeVar
import jwt
from pydantic import BaseModel

from app.shared.core.errors.result_errors.token_errors import TokenErrors
from app.shared.core.result.result import Result

Payload = TypeVar("Payload", bound=BaseModel)


class JwtTokenService(Generic[Payload]):
    secret: str
    expirationTime: int
    algorithm: str = "HS256"

    @classmethod
    def get_token(cls, payload: Payload) -> tuple[str, int]:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        payload_data = payload.model_dump()
        payload_data["exp"] = expire
        return (
            jwt.encode(payload.model_dump(), cls.secret, algorithm=cls.algorithm),
            int(expire.timestamp()),
        )

    @classmethod
    @abstractmethod
    def parse_token(cls, token: str) -> Result[Payload]:
        pass
