from platformdirs import user_documents_dir
from pydantic import field_validator
from app.shared.core.serializer import DbSerializer, Serializer
from app.users.domain.user import UserEntity
from app.users.dtos.user_dto import UserDto


class UserSerializer(DbSerializer):
    id: str
    email: str

    @classmethod
    def serialize(cls, data: UserEntity) -> "UserSerializer":
        return UserSerializer(
            id=data.id,
            email=data.email,
            created_at=data.created_at,
            updated_at=data.updated_at,
        )
