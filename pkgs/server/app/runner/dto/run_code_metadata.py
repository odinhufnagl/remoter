from pydantic import BaseModel


class RunCodeMetadataDto(BaseModel):
    mounts: list[tuple[str, str | None]]
