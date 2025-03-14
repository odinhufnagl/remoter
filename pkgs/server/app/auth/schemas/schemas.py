from pydantic import BaseModel, EmailStr, field_validator, validator


class RequestBodySignup(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    def password_must_be_valid(cls, v):
        if len(v) < 8:
            raise ValueError("password must be at least 8 characters")
        return v


class RequestBodyLogin(BaseModel):
    email: str
    password: str


class RequestBodyRefreshToken(BaseModel):
    refresh_token: str


class RequestBodyLogout(BaseModel):
    refresh_token: str
