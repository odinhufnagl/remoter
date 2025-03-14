from unittest.mock import patch
import uuid

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import insert
from sqlmodel import Session, select
from app.database.models.user import UserModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine

from tests.api.e2e.auth.auth_credentials import verify_auth_credentials
from tests.api.e2e.client import client, session


def api_login(client, email: str, password: str):
    return client.post(
        "/api/v1/auth/login", json={"email": email, "password": password}
    )


@pytest.mark.asyncio
async def test_login_wrong_password(client: TestClient, session: AsyncSession):
    email = "johndoe@johndoe.com"
    password = "correctpassword"
    user = UserModel(email=email, id=str(uuid.uuid4()))
    user.password = password
    session.add(user)
    await session.commit()

    response = api_login(client, email, "wrongpassword")
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["error"]["message"] == "Incorrect username or password"


@pytest.mark.asyncio
async def test_login_correct_password(client: TestClient, session: AsyncSession):
    email = "johndoe@johndoe.com"
    password = "correctpassword"
    user = UserModel(email=email, id=str(uuid.uuid4()))
    user.password = password
    session.add(user)
    await session.commit()

    response = api_login(client, email, password)
    assert response.status_code == 200, response.text
    await verify_auth_credentials(response.json(), user.id, session)


@pytest.mark.asyncio
async def test_login_unknown_email(client: TestClient, session: AsyncSession):
    email = "johndoe@johndoe.com"
    password = "correctpassword"
    user = UserModel(email=email, id=str(uuid.uuid4()))
    user.password = password
    session.add(user)
    await session.commit()

    response = api_login(client, "otheremail@otheremail.com", password)
    assert response.status_code == 401, response.text
    data = response.json()
    data = response.json()
    assert data["error"]["message"] == "Incorrect username or password"
