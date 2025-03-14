import datetime

from fastapi.responses import JSONResponse


from app.shared.core.errors.error_status_mappping import RESULT_ERROR_STATUS_MAPPING
from app.shared.core.errors.result_errors.db_errors import DB_ERROR_CODES
from app.shared.core.errors.result_errors.user_errors import USER_ERROR_CODES
from app.shared.core.result.result_error import ResultError

ERROR_CODE_MAPPING = {
    DB_ERROR_CODES["UNKNOWN_DB_ERROR"]: 500,
    USER_ERROR_CODES["NOT_FOUND"]: 404,
}


class ResponseError:
    def __init__(self, error: dict, status_code: int):
        self.error = error
        self.status_code = status_code
        self.timestamp = datetime.datetime.now()

    def __str__(self):
        return f"{self.error['message']}"

    def __repr__(self):
        return f"{self.error['message']}"

    def to_dict(self):
        return {
            "error": self.error,
            "timestamp": self.timestamp,
        }

    def json_response(self):
        return JSONResponse(
            status_code=self.status_code,
            content={
                "error": self.error,
                "timestamp": self.timestamp.isoformat(),
            },
        )

    @staticmethod
    def from_result_error(result_error: ResultError):
        status_code = RESULT_ERROR_STATUS_MAPPING[result_error.code]
        error_data = result_error.public_data
        if error_data:
            error = {
                "message": result_error.message,
                "error_code": result_error.code,
                "data": error_data,
            }
        else:
            error = {"message": result_error.message, "error_code": result_error.code}
        return ResponseError(error=error, status_code=status_code)
