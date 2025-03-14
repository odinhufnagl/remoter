from pydantic import BaseModel
from app.auth.types.auth_credentials import AuthCredentials
from app.shared.core.serializer import Serializer


class AuthCredentialsSerializer(Serializer):
    access_token: str
    refresh_token: str

    @classmethod
    def serialize(cls, access_token: str, refresh_token: str, expires_in: int):
        return cls(
            access_token=access_token,
            refresh_token=refresh_token,
        )
