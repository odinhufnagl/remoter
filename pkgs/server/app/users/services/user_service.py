from app.shared.core.result.result import Result
from app.users.domain.user import UserEntity
from app.users.repos.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_user_by_id(self, id: str) -> Result[UserEntity]:
        return await self.user_repository.get_user_by_id(id)
