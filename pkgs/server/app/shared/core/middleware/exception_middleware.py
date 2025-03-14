from unittest import result
from venv import logger
from fastapi import Request
import logging
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.shared.core.errors.response_errors_mapping import (
    map_exception_to_response_error,
)
from app.shared.core.errors.result_errors.db_errors import DB_ERROR_CODES
from app.shared.core.errors.result_errors.user_errors import USER_ERROR_CODES


class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            return map_exception_to_response_error(exc)
