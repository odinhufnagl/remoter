from app.shared.core.errors.result_errors.user_errors import USER_ERROR_CODES


RESULT_ERROR_STATUS_MAPPING = {
    # USER_ERROR_CODES
    2001: 404,
    2002: 400,
    # DB_ERROR_CODES
    5000: 500,
    6001: 401,
    # DEFAULT_RESULT_ERROR_CODES
    1000: 500,
    7000: 401,
    7001: 401,
}
