from fastapi import Depends
from app.database.dependencies import get_db_session
from app.users.repos.user_repository import UserRepository
from app.users.services.user_service import UserService


def get_user_repo(db=Depends(get_db_session)) -> UserRepository:
    return UserRepository(db)


def get_user_service(user_repo=Depends(get_user_repo)) -> UserService:
    return UserService(user_repository=user_repo)
