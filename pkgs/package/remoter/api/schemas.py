from typing import Any, Optional
from pydantic import BaseModel


class RunCodeResponse(BaseModel):
    return_value: Optional[Any] = None
    mounted_data_bytes: Optional[bytes] = None
    logs: str
    is_error: bool
    stderr: str
