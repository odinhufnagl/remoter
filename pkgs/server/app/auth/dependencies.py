from fastapi import Depends
from app.auth.repos.token_repository import TokenRepository
from app.auth.services.access_token_service import AccessTokenService
from app.auth.services.auth_service import AuthService
from app.auth.services.refresh_token_service import RefreshTokenService
from app.database.dependencies import get_db_session
from app.users.dependencies import get_user_repo
from app.users.repos.user_repository import UserRepository
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


def get_access_token_service() -> AccessTokenService:
    return AccessTokenService()


def get_refresh_token_service() -> RefreshTokenService:
    return RefreshTokenService()


def get_token_repository(
    db_session: AsyncSession = Depends(get_db_session),
) -> TokenRepository:
    return TokenRepository(db_session)


def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repo),
    access_token_service: AccessTokenService = Depends(get_access_token_service),
    refresh_token_service: RefreshTokenService = Depends(get_refresh_token_service),
    token_repository: TokenRepository = Depends(get_token_repository),
    db_session: AsyncSession = Depends(get_db_session),
) -> AuthService:
    return AuthService(
        user_repository=user_repository,
        access_token_service=access_token_service,
        refresh_token_service=refresh_token_service,
        token_repository=token_repository,
        db_session=db_session,
    )
