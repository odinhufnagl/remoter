from fastapi import BackgroundTasks
from app.file_storage.file_storage_service import FileStorageService
from app.file_storage.output_file_storage_service import OutputFileStorageService
from .use_cases.run_code_use_case import RunCodeUseCase


def get_run_code_use_case() -> RunCodeUseCase:
    return RunCodeUseCase()


def get_file_storage_service(background_tasks: BackgroundTasks) -> FileStorageService:
    return FileStorageService(background_tasks)


def get_output_file_storage_service(
    background_tasks: BackgroundTasks,
) -> OutputFileStorageService:
    return OutputFileStorageService(get_file_storage_service(background_tasks))
