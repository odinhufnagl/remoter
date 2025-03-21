import re
from fastapi import APIRouter, Depends
from sqlalchemy import select
from app.auth.dependencies import get_api_key_service, get_auth_service
from app.auth.errors.auth_errors import AuthError, AuthErrors
from app.auth.schemas.schemas import (
    RequestBodyLogin,
    RequestBodyRefreshToken,
    RequestBodySignup,
)
from app.auth.serializers.api_key_serializer import ApiKeySerializer
from app.auth.serializers.auth_credentials_serializer import AuthCredentialsSerializer
from app.auth.services import auth_service
from app.auth.services.api_key_service import ApiKeyService
from app.auth.services.auth_service import AuthService
from app.database.models import api_key
from app.database.models.user import UserModel
from app.shared.core.auth import UserInfo
from app.database.dependencies import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.shared.core.dependencies.auth import get_current_user
from app.users.dependencies import get_user_service
from app.users.serializers.user_serializer import UserSerializer
from app.users.services.user_service import UserService
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

router = APIRouter()


@router.post("/login", tags=["auth"])
async def login(
    body: RequestBodyLogin,
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        result = await auth_service.login(email=body.email, password=body.password)
        if result.is_failure():
            raise result.error.exc()
        creds = result.get_value()
        return AuthCredentialsSerializer(
            access_token=creds.access_token,
            refresh_token=creds.refresh_token,
        )
    except Exception as e:
        print("hello wowwowowo", e)
        raise AuthErrors.login_fail().exc()


@router.post("/signup", tags=["auth"])
async def signup(
    body: RequestBodySignup,
    auth_service: AuthService = Depends(get_auth_service),
):

    result = await auth_service.signup(email=body.email, password=body.password)
    if result.is_failure():
        raise result.error.exc()

    creds = result.get_value()
    return AuthCredentialsSerializer(
        access_token=creds.access_token,
        refresh_token=creds.refresh_token,
    )


@router.post("/logout", tags=["auth"])
async def logout(
    user_info: UserInfo = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service),
):

    result = await auth_service.logout(user_info.user_id)
    if result.is_failure():
        raise result.error.exc()
    return


@router.post("/refresh", tags=["auth"])
async def refresh_token(
    body: RequestBodyRefreshToken, auth_service: AuthService = Depends(get_auth_service)
):
    result = await auth_service.refresh_token(body.refresh_token)
    if result.is_failure():
        raise result.error.exc()
    creds = result.get_value()
    return AuthCredentialsSerializer(
        access_token=creds.access_token,
        refresh_token=creds.refresh_token,
    )


@router.get("/self", tags=["auth"])
async def self(
    user_info: UserInfo = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    user_result = await user_service.get_user_by_id(user_info.user_id)
    if user_result.is_failure():
        raise user_result.error.exc()
    user = user_result.get_value()
    return UserSerializer.serialize(user)


@router.post("/api-key", tags=["auth"])
async def post_api_key(
    user_info: UserInfo = Depends(get_current_user),
    api_key_service: ApiKeyService = Depends(get_api_key_service),
):
    result = await api_key_service.create_api_key(user_info.user_id)
    print("rrrhah", result)
    if result.is_failure():
        raise result.error.exc()
    return ApiKeySerializer(api_key=result.get_value())
