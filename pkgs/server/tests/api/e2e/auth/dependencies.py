from re import S
from unittest.mock import patch
import uuid

from fastapi import Depends
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import insert
from sqlmodel import Session, select
from app.auth.dependencies import get_auth_service
from app.auth.repos.token_repository import TokenRepository
from app.auth.services.access_token_service import (
    AccessTokenPayload,
    AccessTokenService,
)
from app.auth.services.auth_service import AuthService
from app.auth.services.refresh_token_service import (
    RefreshTokenPayload,
    RefreshTokenService,
)
from app.database.models.token import TokenModel
from app.database.models.user import UserModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine

from app.users.repos.user_repository import UserRepository
from tests.api.e2e.auth.auth_credentials import verify_auth_credentials
from tests.api.e2e.client import client, session


def auth_service(session: AsyncSession):
    return AuthService(
        UserRepository(session),
        AccessTokenService(),
        RefreshTokenService(),
        TokenRepository(session),
        session,
    )
