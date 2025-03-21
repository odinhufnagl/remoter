from app.auth.repos.api_key_repository import ApiKeyRepository
from app.shared.core.result.result import Result
from app.shared.core.result.result_error import ResultError
import secrets


class ApiKeyService:
    PUBLIC_KEY_LENGTH = 8

    def public_key_from_api_key(self, api_key: str) -> str:
        return api_key[: self.PUBLIC_KEY_LENGTH]

    def generate_api_key(self) -> tuple[str, str]:
        full_api_key = secrets.token_urlsafe(32)
        public_part = full_api_key[: self.PUBLIC_KEY_LENGTH]
        return public_part, full_api_key

    def __init__(self, api_key_repository: ApiKeyRepository):
        self.api_key_repository = api_key_repository

    async def create_api_key(self, user_id: str) -> Result[str, ResultError]:
        public_key, api_key = self.generate_api_key()
        result = await self.api_key_repository.create_api_key(
            user_id, api_key, public_key
        )
        if result.is_failure():
            return Result.fail(result.error)

        return Result.ok(api_key)

    async def get_user_id_by_api_key(self, api_key: str) -> Result[str, ResultError]:
        public_key = self.public_key_from_api_key(api_key)
        return await self.api_key_repository.get_user_id_by_api_key_and_public(
            api_key, public_key
        )
