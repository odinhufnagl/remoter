import os
import shutil
import tempfile
import time

from fastapi import BackgroundTasks

from app.file_storage import file_storage_service
from app.file_storage.file_storage_service import FileStorageService
from pathlib import Path


def remove_file_after_delay(file_path: str, delay: int = 300):
    time.sleep(delay)
    try:
        os.remove(file_path)
        print(f"Deleted {file_path} after {delay} seconds.")
    except Exception as e:
        print(f"Error deleting file: {e}")


class OutputFileStorageService:
    def __init__(self, file_storage_service: FileStorageService) -> None:
        self.file_storage_service = file_storage_service

    def save_file(self, path: str, session_id: str):
        dest_path = Path(self.file_storage_service.save_file(path, f"{session_id}"))
        return dest_path

    def get_file_path(self, session_id: str):
        return os.path.join("/tmp", session_id, "output.zip")
