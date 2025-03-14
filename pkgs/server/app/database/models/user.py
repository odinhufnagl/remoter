import re
from wsgiref import validate
from sqlalchemy import String
from app.database.database import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
import uuid
from sqlalchemy.dialects.postgresql import UUID
from passlib.context import CryptContext
from sqlalchemy.orm import validates
from sqlalchemy import Column, DateTime, create_engine, func

from app.shared.regex import regex_email

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserModel(BaseModel):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda *args, **kwargs: str(uuid.uuid4()),
        index=True,
    )
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)

    @property
    def password(self):
        raise AttributeError("Password is write-only.")

    @password.setter
    def password(self, plain_password: str):
        self.password_hash = pwd_context.hash(plain_password)

    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.password_hash)

    @validates("email")
    def validate_email(self, key, address):
        if not regex_email(address):
            raise ValueError(f"Invalid email address: {address}")
        return address
