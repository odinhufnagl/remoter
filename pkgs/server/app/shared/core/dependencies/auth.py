from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2, OAuth2PasswordBearer

from app.auth.dependencies import get_access_token_service
from app.auth.errors.auth_errors import AuthErrors
from app.auth.services.access_token_service import AccessTokenService
from app.shared.core.auth import UserInfo


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    access_token_service: AccessTokenService = Depends(get_access_token_service),
) -> UserInfo:
    payload_result = access_token_service.parse_token(token)
    if payload_result.is_failure():
        raise AuthErrors.invalid_credentials().exc()
    payload = payload_result.get_value()
    user_info = UserInfo(user_id=payload.user_id)
    return user_info
