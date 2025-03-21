import os
import shutil
import tempfile
import uuid
from zipfile import ZipFile

from requests import session
from sqlalchemy import result_tuple
from app.runner.dto.run_code_metadata import RunCodeMetadataDto
from app.shared.core.result.result import Result
from app.shared.core.result.result_error import ResultError
from app.runner.machine.machine_interface import (
    MachineRunResponse,
    build_and_run_machine,
)


class RunCodeUseCase:

    def __init__(self):
        pass

    async def execute(
        self, folder_path: str, zipf: ZipFile, run_code_metadata: RunCodeMetadataDto
    ) -> Result[MachineRunResponse, ResultError]:
        session_id = str(uuid.uuid4())

        input_path = os.path.join(folder_path, "input")
        output_path = os.path.join(folder_path, "output")
        os.mkdir(input_path)
        os.mkdir(output_path)
        zipf.extractall(input_path)
        print(f"Extracted zip contents to: {folder_path}")

        result = await build_and_run_machine(
            folder_path, session_id, run_code_metadata.mounts
        )
        return result
