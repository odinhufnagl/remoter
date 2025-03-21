import enum
import re
from typing import Optional
from wsgiref import validate
from annotated_types import T
from sqlalchemy import ForeignKey, String, ARRAY
from app.database.database import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
import uuid
from passlib.context import CryptContext


# these will be hardcoded (for now)


class ProcessorModel(BaseModel):
    __tablename__ = "processors"

    # cpu | gpu
    type: Mapped[str] = mapped_column(
        String,
    )
    # intel-x | ...
    name: Mapped[str] = mapped_column(String)
