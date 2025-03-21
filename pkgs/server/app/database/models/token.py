import re
from wsgiref import validate
from sqlalchemy import ForeignKey, String
from app.database.database import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
import uuid
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TokenModel(BaseModel):
    __tablename__ = "refresh_tokens"

    user_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("users.id"),
        unique=True,
        index=True,
    )
    token_hash: Mapped[str] = mapped_column(String, nullable=False)

    @property
    def value(self):
        raise AttributeError("Value is write-only.")

    def verify_token(self, plain_token: str) -> bool:
        return pwd_context.verify(plain_token, self.token_hash)

    @value.setter
    def value(self, plain_token: str):
        self.token_hash = pwd_context.hash(plain_token)
