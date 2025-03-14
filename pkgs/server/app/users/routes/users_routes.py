from fastapi import APIRouter, Depends
from app.users.dependencies import get_user_service
from app.users.serializers.user_serializer import UserSerializer
from app.users.services.user_service import UserService

router = APIRouter()


@router.get("/{user_id}", tags=["users"])
async def get_user(user_id: str, user_service: UserService = Depends(get_user_service)):
    result = await user_service.get_user_by_id(user_id)
    if result.is_failure():
        raise result.error.exc()
    return UserSerializer.serialize(result.get_value())
