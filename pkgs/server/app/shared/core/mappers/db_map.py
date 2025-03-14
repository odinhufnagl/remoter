from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from pydantic import BaseModel


DomainType = TypeVar("DomainType")
DbType = TypeVar("DbType")


class DbMap(ABC, BaseModel, Generic[DomainType, DbType]):
    @classmethod
    @abstractmethod
    def to_domain(cls, db_entity: DbType) -> DomainType:
        raise NotImplementedError("Subclasses must implement the to_domain method.")

    @classmethod
    @abstractmethod
    def to_db(cls, domain_entity: DomainType) -> DbType:
        raise NotImplementedError("Subclasses must implement the to_db method.")

    @classmethod
    def to_domain_bulk(cls, db_entities: list[DbType]) -> list[DomainType]:
        return [cls.to_domain(db_entity) for db_entity in db_entities]
