from unittest.mock import patch
import uuid

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import insert
from sqlmodel import Session, select
from app.database.models.token import TokenModel
from app.database.models.user import UserModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine

from tests.api.e2e.auth.auth_credentials import verify_auth_credentials
from tests.api.e2e.client import client, session


def api_signup(client, email: str, password: str):
    return client.post(
        "/api/v1/auth/signup", json={"email": email, "password": password}
    )


@pytest.mark.asyncio
async def test_signup_bad_email(client: TestClient, session: AsyncSession):
    email = "johndoejohndoe.com"
    password = "correctpassword"
    response = api_signup(client, email, password)
    assert response.status_code == 422, response.text


@pytest.mark.asyncio
async def test_signup_bad_password(client: TestClient, session: AsyncSession):
    email = "johndoe@johndoe.com"
    password = "short"

    response = api_signup(client, email, password)
    assert response.status_code == 422, response.text


@pytest.mark.asyncio
async def test_signup_good_email_and_password(
    client: TestClient, session: AsyncSession
):
    email = "johndoe@johndoe.com"
    password = "correctpassword"
    response = api_signup(client, email, password)
    db_user = (
        await session.execute(select(UserModel).where(UserModel.email == email))
    ).scalar_one_or_none()
    print("dbdbdbd", db_user)
    assert db_user
    assert db_user.email == email
    assert db_user.verify_password(password)
    assert response.status_code == 200, response.text
    data = response.json()
    await verify_auth_credentials(data, db_user.id, session)
