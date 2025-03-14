from abc import ABC
from typing import Generic, TypeVar


ValueObjectProps = TypeVar("ValueObjectProps")


class ValueObject(ABC, Generic[ValueObjectProps]):
    def __init__(self, props: ValueObjectProps) -> None:
        self._props = props

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return other._props == self._props

    def __hash__(self) -> int:
        return hash(self._props)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._props})"

    def __str__(self) -> str:
        return str(self._props)

    @property
    def value(self) -> ValueObjectProps:
        return self._props
