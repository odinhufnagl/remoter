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
from tests.api.e2e.auth.dependencies import auth_service
from tests.api.e2e.client import client, session


def api_logout(client, access_token):
    return client.post(
        "/api/v1/auth/logout", headers={"Authorization": f"Bearer {access_token}"}
    )


@pytest.mark.asyncio
async def test_logout_wrong_token(client: TestClient, session: AsyncSession):
    access_token = "some-random-token"

    response = api_logout(client, access_token)
    assert response.status_code == 401, response.text
    data = response.json()
    print("dattttt", data)
    assert data["error"]["message"] == "Invalid credentials"


@pytest.mark.asyncio
async def test_logout_token_exist(
    client: TestClient,
    session: AsyncSession,
):
    email = "johndoe@johndoe.com"
    password = "somepassword"
    auth_creds = (await auth_service(session).signup(email, password)).get_value()
    user = (
        await session.execute(select(UserModel).where(UserModel.email == email))
    ).scalar_one_or_none()

    assert user

    response = api_logout(client, auth_creds.access_token)
    assert response.status_code == 200, response.text
    db_token_after = (
        await session.execute(select(TokenModel).where(TokenModel.user_id == user.id))
    ).scalar_one_or_none()
    assert db_token_after is None


@pytest.mark.asyncio
async def test_allowed_to_logout_twice(
    client: TestClient,
    session: AsyncSession,
):

    email = "johndoe@johndoe.com"
    password = "correctpassword"

    await session.commit()

    auth_creds = (await auth_service(session).signup(email, password)).get_value()
    user = (
        await session.execute(select(UserModel).where(UserModel.email == email))
    ).scalar_one_or_none()

    response_1 = api_logout(client, auth_creds.access_token)
    assert response_1.status_code == 200, response_1.text
    response_2 = api_logout(client, auth_creds.access_token)
    assert response_2.status_code == 200, response_2.text


@pytest.mark.asyncio
async def test_logout_no_token_provided(client: TestClient, session: AsyncSession):
    response = api_logout(client, "")
    assert response.status_code == 401, response.text


@pytest.mark.asyncio
async def test_logout_fail_using_refresh_token(
    client: TestClient,
    session: AsyncSession,
):
    email = "johndoe@johndoe.com"
    password = "somepassword"
    auth_creds = (await auth_service(session).signup(email, password)).get_value()
    user = (
        await session.execute(select(UserModel).where(UserModel.email == email))
    ).scalar_one_or_none()

    assert user

    response = api_logout(client, auth_creds.refresh_token)
    assert response.status_code == 401, response.text
    db_token_after = (
        await session.execute(select(TokenModel).where(TokenModel.user_id == user.id))
    ).scalar_one_or_none()
    assert db_token_after
