from pydantic import BaseModel


class AuthCredentials(BaseModel):
    access_token: str
    refresh_token: str
