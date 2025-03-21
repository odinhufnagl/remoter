import enum
import re
from typing import Optional
from wsgiref import validate
from annotated_types import T
from sqlalchemy import ForeignKey, Integer, String, ARRAY
from app.database.database import BaseModel
from sqlalchemy.orm import Mapped, mapped_column

from app.database.models.processor import ProcessorModel
from app.runner.domain.runner_session_entity import Processor


class MachineConfigModel(BaseModel):
    __tablename__ = "machine_configs"

    processor_id: Mapped[str] = mapped_column(
        String, ForeignKey("processors.id"), unique=True, nullable=False
    )
    processor: ProcessorModel
    ram_size: Mapped[int] = mapped_column(Integer, nullable=False)
    disk_size: Mapped[int] = mapped_column(Integer, nullable=False)
    created_by: Mapped[str] = mapped_column(
        String, ForeignKey("users.id"), nullable=False, index=True
    )
