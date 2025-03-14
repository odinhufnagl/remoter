from app.shared.core.result.result_error import ResultError


MACHINE_ERROR_CODES = {
    "UNKNOWN_MACHINE_ERROR": 5000,
    "BUILD_ERROR": 5001,
    "RUN_ERROR": 5002,
}


class MachineError(ResultError[None]):
    codes: dict = MACHINE_ERROR_CODES


class MachineErrors:
    @staticmethod
    def unkown_machine_error() -> MachineError:
        return MachineError(
            code=MACHINE_ERROR_CODES["UNKNOWN_MACHINE_ERROR"],
            message="Unknown machine error",
        )

    @staticmethod
    def build_error() -> MachineError:
        return MachineError(
            code=MACHINE_ERROR_CODES["BUILD_ERROR"],
            message="Error building the machine",
        )

    @staticmethod
    def run_error() -> MachineError:
        return MachineError(
            code=MACHINE_ERROR_CODES["RUN_ERROR"],
            message="Error running the machine",
        )
