from typing import Generic, Optional
from pydantic import BaseModel
from typing_extensions import TypeVar
from abc import ABC

from app.shared.core.domain_entity import Props


Props = TypeVar("Props", default=None)


class ResultErrorException(Exception, Generic[Props]):
    def __init__(self, error: "ResultError[Props]"):
        self.error = error

    def __repr__(self) -> str:
        return f"ResultErrorException({self.error})"

    def __str__(self) -> str:
        return f"ResultErrorException({self.error})"


ResultErrorPropsType = TypeVar("ResultErrorPropsType")


DEFAULT_RESULT_ERROR_CODES = {
    "UNKNOWN_ERROR": 1000,
}


class ResultError(Generic[ResultErrorPropsType]):
    code: int
    message: str
    props: Optional[ResultErrorPropsType] = None

    def __init__(
        self,
        code: Optional[int] = None,
        message: Optional[str] = None,
        props=None,
    ):
        self.code = code if code is not None else self.__class__.code
        self.message = message if message is not None else self.__class__.message
        self.props = props

    @property
    def public_data(self) -> dict | None:
        return None

    def __str__(self) -> str:
        return f"Error Code: {self.code}, Message: {self.message}"

    codes: dict = DEFAULT_RESULT_ERROR_CODES

    def exc(self):
        return ResultErrorException(error=self)


class DefaultResultErrors:
    @staticmethod
    def unknown_error() -> "ResultError":
        return ResultError(
            code=DEFAULT_RESULT_ERROR_CODES["UNKNOWN_ERROR"], message="Unknown error"
        )
