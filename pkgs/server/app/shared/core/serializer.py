from abc import ABC, abstractmethod
import datetime
from turtle import update
from typing import Generic, Self, TypeVar

from pydantic import BaseModel, field_validator, validator


class Serializer(BaseModel, ABC):

    @classmethod
    @abstractmethod
    def serialize(cls, *args, **kwargs) -> Self:
        pass


class DbSerializer(Serializer):

    created_at: datetime.datetime
    updated_at: datetime.datetime

    @field_validator("created_at", "updated_at")
    def must_be_present(cls, v):
        if v is None:
            raise ValueError("Timestamp must not be null")
        return v
