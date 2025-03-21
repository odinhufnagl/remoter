import datetime
import enum
from platform import machine
from re import S
from typing import Optional, Self

from pydantic import BaseModel

from app.shared.core.domain_entity import DomainEntity, DomainId
from app.shared.core.result.result import Result
from app.shared.core.result.result_error import ResultError
from app.shared.core.value_object import ValueObject


class ProcessorProps(BaseModel):
    id: str
    type: str
    name: str


class Processor(ValueObject[ProcessorProps]):
    @property
    def id(self) -> str:
        return self._props.id


class MachineConfigProps(BaseModel):
    created_by: str
    processor: Processor
    ram_size: int
    disk_size: int


class MachineConfig(DomainEntity[MachineConfigProps]):
    @property
    def disk_size(self) -> int:
        return self.props.disk_size

    @property
    def ram_size(self) -> int:
        return self.props.ram_size

    @property
    def created_by(self) -> str:
        return self.props.created_by

    @property
    def processor(self) -> Processor:
        return self.props.processor


class RunnerSessionStatus(enum.Enum):
    NOT_STARTED = "not_started"
    STARTING = "starting"
    RUNNING = "running"
    SUCCESS = "finished"
    ERROR = "error"


class RunnerSessionEntityProps(BaseModel):
    machine_config: MachineConfig
    machine_session_id: str
    user_id: str
    status: RunnerSessionStatus
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None


class RunnerSessionEntity(DomainEntity[RunnerSessionEntityProps]):
    @property
    def user_id(self) -> str:
        return self.props.user_id

    @classmethod
    def create(
        cls,
        id: DomainId,
        machine_session_id: str,
        user_id: str,
        status: RunnerSessionStatus,
        machine_config: MachineConfig,
    ) -> Result[Self, ResultError]:
        props = RunnerSessionEntityProps(
            machine_session_id=machine_session_id,
            user_id=user_id,
            status=status,
            machine_config=machine_config,
        )
        return Result.ok(cls(id=id, props=props))
