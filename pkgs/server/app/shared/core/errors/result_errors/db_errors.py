from app.shared.core.result.result_error import ResultError

DB_ERROR_CODES = {
    "UNKNOWN_DB_ERROR": 5000,
}


class DbError(ResultError):
    codes: dict = DB_ERROR_CODES


class DbErrors:
    @staticmethod
    def unkown_db_error() -> "DbError":
        return DbError(
            code=DB_ERROR_CODES["UNKNOWN_DB_ERROR"], message="Unknown database error"
        )
