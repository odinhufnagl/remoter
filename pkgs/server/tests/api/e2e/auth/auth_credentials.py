from psycopg import AsyncRawServerCursor
from sqlalchemy import select

from app.auth.services.access_token_service import AccessTokenService
from app.auth.services.refresh_token_service import RefreshTokenService
from app.database.models.token import TokenModel


async def verify_auth_credentials(data, user_id, session):
    assert data["refresh_token"]
    assert data["access_token"]

    db_token = (
        await session.execute(select(TokenModel).where(TokenModel.user_id == user_id))
    ).scalar_one_or_none()
    assert db_token
    assert db_token.verify_token(data["refresh_token"])

    assert AccessTokenService().parse_token(
        data["access_token"]
    ).get_value().user_id == str(user_id)
    assert RefreshTokenService().parse_token(
        data["refresh_token"]
    ).get_value().user_id == str(user_id)
