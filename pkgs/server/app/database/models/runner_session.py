import enum
from annotated_types import T
from sqlalchemy import ForeignKey, String, ARRAY, null
from app.database.database import BaseModel
from sqlalchemy.orm import Mapped, mapped_column

from app.database.models.machine_config import MachineConfigModel
from app.runner.domain.runner_session_entity import MachineConfig, RunnerSessionStatus


class RunnerSessionModel(BaseModel):
    __tablename__ = "runner_sessions"

    user_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("users.id"),
        unique=False,
        index=True,
    )
    machine_config_id: Mapped[str] = mapped_column(
        String, ForeignKey("machine_configs.id"), nullable=False, unique=False
    )

    machine_config: MachineConfigModel
    machine_session_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    status: Mapped[RunnerSessionStatus] = mapped_column(
        String, default=RunnerSessionStatus.NOT_STARTED.value
    )
