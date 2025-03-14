from abc import ABC, abstractmethod
from typing import TypeVar
from typing import Generic, Self
from uuid import uuid4
from pydantic import BaseModel


class DomainId(BaseModel):
    value: str

    @staticmethod
    def generate() -> "DomainId":
        return DomainId(value=str(uuid4()))


Props = TypeVar("Props")


class DomainEntity(ABC, Generic[Props]):

    _id: DomainId
    props: Props

    @property
    def id(self) -> str:
        return self._id.value

    def __init__(self, id: DomainId, props: Props) -> None:
        self._id = id
        self.props = props
