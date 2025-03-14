from pydantic import BaseModel


class RunResponse(BaseModel):
    return_value: str
