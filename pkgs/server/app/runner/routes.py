import io
import json
import os
import tempfile
import zipfile
from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from fastapi.responses import FileResponse
from app.file_storage.file_storage_service import FileStorageService
from app.file_storage.output_file_storage_service import OutputFileStorageService
from app.runner.dependencies import (
    get_file_storage_service,
    get_output_file_storage_service,
    get_run_code_use_case,
)

from app.runner.dto.run_code_metadata import RunCodeMetadataDto
from app.runner.serializers.machine_run_serializer import MachineRunSerializer
from app.runner.use_cases.run_code_use_case import RunCodeUseCase
from app.shared.core.auth import UserInfo
from app.shared.core.dependencies.auth import (
    get_current_user,
    get_current_user_with_api_key_or_token,
)
from app.users.dependencies import get_user_service
from app.users.serializers.user_serializer import UserSerializer
from app.users.services.user_service import UserService
from fastapi import APIRouter, BackgroundTasks, UploadFile, File

router = APIRouter()


@router.post("/run_code", tags=["runner"])
async def run_code(
    file: UploadFile = File(...),
    mounts: str = Form(...),
    run_code_use_case: RunCodeUseCase = Depends(get_run_code_use_case),
    output_file_storage_service: OutputFileStorageService = Depends(
        get_output_file_storage_service
    ),
    user_info: UserInfo = Depends(get_current_user_with_api_key_or_token),
):

    zip_contents = await file.read()

    with zipfile.ZipFile(io.BytesIO(zip_contents)) as zf:
        with tempfile.TemporaryDirectory() as tmp_folder_path:
            result = await run_code_use_case.execute(
                tmp_folder_path, zf, RunCodeMetadataDto(mounts=json.loads(mounts))
            )
            if result.is_failure():
                raise result.error.exc()
            run_code_response = result.get_value()
            output_zip_file_path = os.path.abspath(result.get_value().output_dir)
            output_file_storage_service.save_file(
                output_zip_file_path,
                run_code_response.session_id,
            )
            return MachineRunSerializer(
                logs=run_code_response.logs,
                session_id=run_code_response.session_id,
                is_error=run_code_response.is_error,
                stderr=run_code_response.stderr,
            )


@router.get("/run_code_download_output/{session_id}", tags=["runner"])
async def run_code_download_output(
    session_id: str,
    output_file_storage_service: OutputFileStorageService = Depends(
        get_output_file_storage_service
    ),
    user_info: UserInfo = Depends(get_current_user_with_api_key_or_token),
):
    try:

        file_path = output_file_storage_service.get_file_path(session_id)
        print("fileeee", file_path)
        return FileResponse(
            file_path, media_type="application/x-zip-compressed", filename="output.zip"
        )
    except Exception as e:
        print("error", e)


@router.get("/runs", tags=["runner"])
async def get_runs(user_info: UserInfo = Depends(get_current_user)):
    pass
