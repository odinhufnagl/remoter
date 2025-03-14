from app.database.models.user import UserModel
from app.shared.core.domain_entity import DomainId
from app.shared.core.mappers.db_map import DbMap
from app.users.domain.user import UserEntity, UserEntityProps


class UserDbMap(DbMap[UserEntity, UserModel]):
    @classmethod
    def to_domain(cls, db_entity: UserModel) -> UserEntity:
        print("db_entity", db_entity.__dict__, db_entity.created_at)
        props = UserEntityProps(
            email=db_entity.email,
            created_at=db_entity.created_at,
            updated_at=db_entity.updated_at,
        )
        id = DomainId(value=db_entity.id)
        return UserEntity(id=id, props=props)

    @classmethod
    def to_db(cls, domain_entity: UserEntity) -> UserModel:
        return UserModel(
            id=domain_entity.id,
            email=domain_entity.email,
        )
