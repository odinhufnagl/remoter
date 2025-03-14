from typing import Optional
from pydantic import BaseModel
from app.shared.core.result.result_error import ResultError


class EntityIdProps(BaseModel):
    id: Optional[str]


class EntityNotFoundError(ResultError[EntityIdProps]):
    pass


class EntityAlreadyExistError(ResultError[EntityIdProps]):
    @property
    def public_data(self) -> dict:
        if not self.props:
            raise ValueError("Props must be defined on subclass")
        return {"id": self.props.id}
