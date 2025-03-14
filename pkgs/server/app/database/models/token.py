import re
from wsgiref import validate
from sqlalchemy import String
from app.database.database import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
import uuid
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TokenModel(BaseModel):
    __tablename__ = "refresh_token"
    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda *args, **kwargs: str(uuid.uuid4()),
    )
    user_id: Mapped[str] = mapped_column(
        String,
        unique=True,
        default=lambda *args, **kwargs: str(uuid.uuid4()),
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
