from typing import Generic, Optional, Self
from typing_extensions import TypeVar
from app.shared.core.result.result_error import ResultError


Success = TypeVar("Success")
Failure = TypeVar("Failure", bound="ResultError", default="ResultError", covariant=True)


class Result(Generic[Success, Failure]):
    def __init__(
        self,
        success: bool,
        value: Optional[Success] = None,
        error: Optional[Failure] = None,
    ):
        self.success = success
        self.value = value
        self._error = error

    @classmethod
    def ok(cls, value: Optional[Success]) -> Self:
        return cls(success=True, value=value)

    @classmethod
    def fail(cls, error: Optional[Failure]) -> Self:
        return cls(success=False, error=error)

    def __str__(self):
        if self.success:
            return f"Success: {self.value}"
        else:
            return f"Failure: {self._error}"

    def is_failure(self):
        return not self.success

    def is_success(self):
        return self.success

    def get_value(self) -> Success:
        if self.value == None:
            raise ValueError("Value is None")
        return self.value

    @property
    def error(self) -> Failure:
        if self._error == None:
            raise ValueError("Error is None")
        return self._error


def test(input: int) -> Result[int]:
    if input == 2:
        return Result[int].ok(20)
    return Result[int].ok(20)
