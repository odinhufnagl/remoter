from typing import Generic, Optional, TypeVar
from typing import Any

ReturnValueType = TypeVar("ReturnValueType", bound=Any)


class ResponseCollector(Generic[ReturnValueType]):
    file_paths: list[tuple[str, Optional[str]]] = []
    return_value: ReturnValueType

    def __init__(self) -> None:
        pass

    def set_file(
        self, remote_file_path: str, local_file_path: Optional[str] = None
    ) -> None:
        self.file_paths.append((remote_file_path, local_file_path))

    def set_return_value(self, value: ReturnValueType) -> None:
        self.return_value = value
