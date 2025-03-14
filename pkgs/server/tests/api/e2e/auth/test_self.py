from re import S
from unittest.mock import patch
import uuid

from fastapi import Depends
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import insert
from sqlmodel import Session, select

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
from tests.api.e2e.auth.dependencies import auth_service
from tests.api.e2e.client import client, session


def api_self(client, access_token):
    return client.post(
        "/api/v1/auth/self", headers={"Authorization": f"Bearer {access_token}"}
    )


@pytest.mark.asyncio
async def test_receives_self(client: TestClient, session: AsyncSession):
    email = "johndoe@johndoe.com"
    password = "somepassword"
    auth_creds = (await auth_service(session).signup(email, password)).get_value()
    user = (
        await session.execute(select(UserModel).where(UserModel.email == email))
    ).scalar_one_or_none()
    assert user
    response = api_self(client, auth_creds.access_token)
    assert response.status_code == 200, response.text
    data = response.json()

    assert data["email"] == email
    assert data["id"] == user.id
    assert data.get("password") is None


@pytest.mark.asyncio
async def test_return_unauthorized_if_wrong_token(
    client: TestClient,
    session: AsyncSession,
):
    access_token = "random-token"

    response = api_self(client, access_token)
    assert response.status_code == 401, response.text
