from sqlalchemy import ForeignKey, String
from app.database.database import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from passlib.context import CryptContext


class ApiKeyModel(BaseModel):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    __tablename__ = "api_keys"

    user_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("users.id"),
        unique=False,
        index=True,
    )
    public_key: Mapped[str] = mapped_column(
        String, nullable=False, unique=False, index=True
    )
    api_key_hash: Mapped[str] = mapped_column(String, nullable=False, index=True)

    @property
    def value(self):
        raise AttributeError("Value is write-only.")

    def verify_api_key(self, plain_api_key: str) -> bool:
        return self.pwd_context.verify(plain_api_key, self.api_key_hash)

    @value.setter
    def value(self, plain_api_key: str):
        self.api_key_hash = self.pwd_context.hash(plain_api_key)
