import os
import shutil
import tempfile
import time

from fastapi import BackgroundTasks


def remove_file_after_delay(file_path: str, delay: int = 300):
    time.sleep(delay)
    try:
        os.remove(file_path)
        print(f"Deleted {file_path} after {delay} seconds.")
    except Exception as e:
        print(f"Error deleting file: {e}")


class FileStorageService:
    def __init__(self, background_tasks: BackgroundTasks) -> None:
        self.background_tasks = background_tasks

    def save_file(self, path: str, storage_folder):
        temp_dir = tempfile.gettempdir()

        destination_dir = os.path.join(temp_dir, storage_folder)
        os.makedirs(destination_dir, exist_ok=True)

        destination_path = os.path.join(destination_dir, os.path.basename(path))
        print("Saving file from:", path, "to:", destination_path)

        shutil.copy(path, destination_path)  # Copy file safely
        print("lslslsl", os.listdir(destination_dir))

        #     self.background_tasks.add_task(remove_file_after_delay, destination_path)

        return destination_path

    def get_file(self, path: str):
        with open(path, "rb") as f:
            return f.read()
