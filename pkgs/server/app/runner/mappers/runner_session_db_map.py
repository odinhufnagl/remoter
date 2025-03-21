from ssl import create_default_context
from app.database.models.machine_config import MachineConfigModel
from app.database.models.processor import ProcessorModel
from app.database.models.runner_session import RunnerSessionModel
from app.database.models.user import UserModel
from app.runner.domain.runner_session_entity import (
    MachineConfig,
    MachineConfigProps,
    Processor,
    ProcessorProps,
    RunnerSessionEntity,
    RunnerSessionEntityProps,
)
from app.shared.core.domain_entity import DomainId
from app.shared.core.mappers.db_map import DbMap


class RunnerSessionDbMap(DbMap[RunnerSessionEntity, RunnerSessionModel]):

    @classmethod
    def to_domain(cls, db_entity: RunnerSessionModel) -> RunnerSessionEntity:
        print("db_entity", db_entity.__dict__, db_entity.created_at)

        props = RunnerSessionEntityProps(
            machine_session_id=db_entity.machine_session_id,
            status=db_entity.status,
            user_id=db_entity.user_id,
            created_at=db_entity.created_at,
            updated_at=db_entity.updated_at,
            machine_config=MachineConfigDbMap.to_domain(db_entity.machine_config),
        )

        id = DomainId(value=db_entity.id)
        return RunnerSessionEntity(id=id, props=props)

    @classmethod
    def to_domain_bulk(
        cls, db_entities: list[RunnerSessionModel]
    ) -> list[RunnerSessionEntity]:
        return super().to_domain_bulk(db_entities)


class MachineConfigDbMap(DbMap[MachineConfig, MachineConfigModel]):
    @classmethod
    def to_domain(cls, db_entity: MachineConfigModel) -> MachineConfig:
        return MachineConfig(
            id=DomainId(value=db_entity.id),
            props=MachineConfigProps(
                ram_size=db_entity.ram_size,
                processor=ProcessorDbMap.to_domain(db_entity.processor),
                disk_size=db_entity.disk_size,
                created_by=db_entity.created_by,
            ),
        )

    @classmethod
    def to_db(cls, domain_entity: MachineConfig) -> MachineConfigModel:
        return MachineConfigModel(
            ram_size=domain_entity.ram_size,
            disk_size=domain_entity.disk_size,
            created_by=domain_entity.created_by,
            processor_id=domain_entity.processor.id,
        )


class ProcessorDbMap(DbMap[Processor, ProcessorModel]):
    @classmethod
    def to_domain(cls, db_entity: ProcessorModel) -> Processor:
        return Processor(
            props=ProcessorProps(
                type=db_entity.type, name=db_entity.name, id=db_entity.id
            )
        )
