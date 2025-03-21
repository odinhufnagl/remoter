from fastapi import Depends, HTTPException, Security, status
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader, OAuth2, OAuth2PasswordBearer
from app.auth.dependencies import (
    get_access_token_service,
    get_api_key_repository,
    get_api_key_service,
)
from app.auth.errors.auth_errors import AuthErrors
from app.auth.repos.api_key_repository import ApiKeyRepository
from app.auth.services.access_token_service import AccessTokenService
from app.auth.services.api_key_service import ApiKeyService
from app.shared.core.auth import UserInfo
from app.users.dependencies import get_user_repo
from app.users.repos import user_repository
from app.users.repos.user_repository import UserRepository


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repository: UserRepository = Depends(get_user_repo),
    access_token_service: AccessTokenService = Depends(get_access_token_service),
) -> UserInfo:
    if not token:
        raise AuthErrors.invalid_credentials().exc()
    payload_result = access_token_service.parse_token(token)
    if payload_result.is_failure():
        raise AuthErrors.invalid_credentials().exc()
    payload = payload_result.get_value()
    user_result = await user_repository.get_user_by_id(payload.user_id)
    if user_result.is_failure():
        raise AuthErrors.invalid_credentials().exc()
    user_info = UserInfo(user_id=payload.user_id)
    return user_info


api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)


async def get_current_user_with_api_key(
    api_key: str = Security(api_key_header),
    api_key_service: ApiKeyService = Depends(get_api_key_service),
    user_repository: UserRepository = Depends(get_user_repo),
) -> UserInfo:
    if not api_key:
        raise AuthErrors.invalid_credentials().exc()
    user_id_result = await api_key_service.get_user_id_by_api_key(api_key)
    if user_id_result.is_failure():
        raise AuthErrors.invalid_credentials().exc()
    user_id = user_id_result.get_value()
    user_result = await user_repository.get_user_by_id(user_id)
    if user_result.is_failure():
        raise AuthErrors.invalid_credentials().exc()
    user_info = UserInfo(user_id=user_id)
    return user_info


async def get_current_user_with_api_key_or_token(
    api_key: str = Security(api_key_header),
    token: str = Depends(oauth2_scheme),
    api_key_repository: ApiKeyRepository = Depends(get_api_key_repository),
    user_repository: UserRepository = Depends(get_user_repo),
    access_token_service: AccessTokenService = Depends(get_access_token_service),
) -> UserInfo:

    try:
        return await get_current_user_with_api_key(
            api_key=api_key,
            api_key_repository=api_key_repository,
            user_repository=user_repository,
        )
    except Exception as e:

        return await get_current_user(
            token=token,
            user_repository=user_repository,
            access_token_service=access_token_service,
        )
