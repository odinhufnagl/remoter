import logging

from app.shared.core.errors.error_status_mappping import RESULT_ERROR_STATUS_MAPPING
from app.shared.core.errors.response_error import ResponseError
from app.shared.core.result.result_error import (
    DefaultResultErrors,
    ResultError,
    ResultErrorException,
)

logger = logging.getLogger(__name__)


def map_result_error_to_response_error(result_error: ResultError):
    status_code = RESULT_ERROR_STATUS_MAPPING[result_error.code]
    if status_code == 500:
        logger.error(f"Internal Server Error: {result_error}")
        return ResponseError.from_result_error(DefaultResultErrors.unknown_error())
    return ResponseError.from_result_error(result_error)


def map_exception_to_response_error(exc: Exception):
    if isinstance(exc, ResultErrorException):
        result_error = exc.error
        return map_result_error_to_response_error(result_error).json_response()
    return ResponseError.from_result_error(
        DefaultResultErrors.unknown_error()
    ).json_response()
