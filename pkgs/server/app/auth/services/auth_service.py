from fastapi import Depends
from app.auth.repos.token_repository import TokenRepository
from app.auth.services.access_token_service import (
    AccessTokenPayload,
    AccessTokenService,
)
from app.auth.services.refresh_token_service import (
    RefreshTokenPayload,
    RefreshTokenService,
)
from app.auth.types.auth_credentials import AuthCredentials
from app.database.dependencies import get_db_session
from app.shared.core.domain_entity import DomainId
from app.shared.core.errors.result_errors.token_errors import TokenErrors
from app.shared.core.errors.result_errors.user_errors import (
    USER_ERROR_CODES,
    UserError,
    UserErrors,
)
from app.shared.core.result.result import Result
from app.shared.core.result.result_error import DefaultResultErrors, ResultError
from app.users.domain.user import UserEntity, UserEntityProps
from app.users.repos import user_repository
from app.users.repos.user_repository import UserRepository
import jwt
from app.config import settings
from sqlalchemy.ext.asyncio import AsyncSession


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository,
        access_token_service: AccessTokenService,
        refresh_token_service: RefreshTokenService,
        token_repository: TokenRepository,
        db_session: AsyncSession = Depends(get_db_session),
    ):
        self.user_repository = user_repository
        self.token_repository = token_repository
        self.access_token_service = access_token_service
        self.refresh_token_service = refresh_token_service
        self.db_session = db_session

    def create_credentials(self, user_id: str) -> AuthCredentials:
        access_token, expires_in = self.access_token_service.get_token(
            AccessTokenPayload(user_id=user_id)
        )
        refresh_token, _ = self.refresh_token_service.get_token(
            RefreshTokenPayload(user_id=user_id)
        )
        return AuthCredentials(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def login(
        self,
        email: str,
        password: str,
        session_incoming: AsyncSession | None = None,
    ) -> Result[AuthCredentials]:
        db_session = session_incoming or self.db_session
        user_result = await self.user_repository.get_by_email_and_password(
            email, password, db_session
        )
        print("user_result", user_result)
        if user_result.is_failure():
            if not session_incoming:
                await db_session.rollback()
            return Result.fail(user_result.error)
        user = user_result.get_value()
        credentials = self.create_credentials(user.id)
        refresh_token_result = await self.token_repository.store_refresh_token(
            user.id, credentials.refresh_token, db_session
        )
        if refresh_token_result.is_failure():
            if not session_incoming:
                await db_session.rollback()
            return Result.fail(refresh_token_result.error)
        if not session_incoming:
            await db_session.commit()

        return Result.ok(credentials)

    async def signup(
        self,
        email: str,
        password: str,
    ) -> Result[AuthCredentials]:

        existing_user_result = await self.user_repository.get_by_email(email)
        if existing_user_result.is_success():
            return Result.fail(
                UserErrors.already_exist(existing_user_result.get_value().id)
            )
        if (
            existing_user_result.is_failure()
            and existing_user_result.error.code != USER_ERROR_CODES["NOT_FOUND"]
        ):
            return Result.fail(existing_user_result.error)
        db_session = self.db_session
        db_session.begin()
        user = UserEntity.create(
            id=DomainId.generate(),
            email=email,
        ).get_value()
        try:
            create_user_result = await self.user_repository.create_user_with_password(
                user, password, db_session
            )
            if create_user_result.is_failure():
                await db_session.rollback()
                return Result.fail(create_user_result.error)
            login_result = await self.login(
                email,
                password,
                db_session,
            )
            if login_result.is_failure():
                await db_session.rollback()
                return Result.fail(login_result.error)
            await db_session.commit()
            return login_result
        except Exception as e:
            await db_session.rollback()
            return Result.fail(DefaultResultErrors.unknown_error())

    async def refresh_token(self, refresh_token: str) -> Result[AuthCredentials]:
        payload_result = self.refresh_token_service.parse_token(refresh_token)
        if payload_result.is_failure():
            return Result.fail(payload_result.error)
        payload = payload_result.get_value()
        token_correct_result = await self.token_repository.get_and_verify_refresh_token(
            payload.user_id, refresh_token
        )
        if token_correct_result.is_failure():
            return Result.fail(token_correct_result.error)
        is_token_correct = token_correct_result.get_value()
        if not is_token_correct:
            return Result.fail(TokenErrors.token_not_correct())
        access_token, _ = self.access_token_service.get_token(
            AccessTokenPayload(user_id=payload.user_id)
        )
        return Result.ok(
            AuthCredentials(access_token=access_token, refresh_token=refresh_token)
        )

    async def logout(self, user_id: str) -> Result[None]:
        result = await self.token_repository.delete_refresh_token(user_id)
        print("babab", result)
        if result.is_failure():
            return Result.fail(result.error)
        return Result.ok(None)
