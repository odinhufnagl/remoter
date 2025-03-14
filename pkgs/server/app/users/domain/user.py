import datetime
from typing import Optional, Self

from click import Option
from pydantic import BaseModel
from app.shared.core.domain_entity import DomainEntity, DomainId
from app.shared.core.result.result import Result
from app.users.domain.user_domain_error import UserDomainError


class UserEntityProps(BaseModel):
    email: str
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None


class UserEntity(DomainEntity[UserEntityProps]):

    @property
    def email(self) -> str:
        return self.props.email

    @property
    def created_at(self) -> datetime.datetime | None:
        return self.props.created_at

    @property
    def updated_at(self) -> datetime.datetime | None:
        return self.props.updated_at

    @classmethod
    def create(
        cls,
        id: DomainId,
        email: str,
    ) -> Result[Self, UserDomainError]:
        props = UserEntityProps(email=email)
        return Result[Self, UserDomainError].ok(cls(id=id, props=props))
