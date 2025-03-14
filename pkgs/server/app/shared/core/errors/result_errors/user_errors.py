from typing import Optional
from app.shared.core.errors.result_errors.common_errors import (
    EntityIdProps,
)
from app.shared.core.result.result_error import ResultError

USER_ERROR_CODES = {"NOT_FOUND": 2001, "ALREADY_EXIST": 2002}


class UserError(ResultError):
    codes: dict = USER_ERROR_CODES
    props: EntityIdProps


class UserNotFoundError(UserError):
    code = USER_ERROR_CODES["NOT_FOUND"]
    props: EntityIdProps

    @property
    def public_data(self):
        return {"id": self.props.id}


class UserAlreadyExistError(UserError):
    code = USER_ERROR_CODES["ALREADY_EXIST"]
    props: EntityIdProps

    @property
    def public_data(self):
        return {"id": self.props.id}


class UserErrors:
    @staticmethod
    def not_found(user_id: Optional[str] = None) -> "UserNotFoundError":
        props = EntityIdProps(id=user_id)
        return UserNotFoundError(
            props=props,
            message=(
                f"User with id: {user_id} not found" if user_id else "User not found"
            ),
        )

    @staticmethod
    def already_exist(user_id: str) -> "UserAlreadyExistError":
        props = EntityIdProps(id=user_id)
        return UserAlreadyExistError(
            props=props, message=f"User with id: {user_id} already exist"
        )
