import os
from zipfile import ZipFile
import zipfile


def add_folders_in_new_folder_in_zipfile(
    zipf: ZipFile, folder_paths: list[str], target_folder_name: str
) -> None:
    for folder in folder_paths:
        folder_basename = os.path.basename(os.path.normpath(folder))
        for root, dirs, files in os.walk(folder):
            for file in files:
                abs_file_path = os.path.join(root, file)

                rel_path = os.path.relpath(abs_file_path, start=folder)

                arcname = os.path.join(target_folder_name, folder_basename, rel_path)
                zipf.write(abs_file_path, arcname=arcname)


def add_folder_to_zip(zipf: ZipFile, local_path: str, zip_target: str) -> None:
    for root, dirs, files in os.walk(local_path):
        for file in files:
            abs_file_path = os.path.join(root, file)

            rel_path = os.path.relpath(abs_file_path, start=local_path)

            arcname = os.path.join(zip_target, rel_path)
            zipf.write(abs_file_path, arcname=arcname)


def sync_folder_with_zip(zip_obj: zipfile.ZipFile, target_dir: str):

    zip_paths = set()
    for info in zip_obj.infolist():
        if info.is_dir():
            continue
        zip_paths.add(info.filename)
        target_file_path = os.path.join(target_dir, info.filename)

        os.makedirs(os.path.dirname(target_file_path), exist_ok=True)

        if os.path.exists(target_file_path):
            current_size = os.path.getsize(target_file_path)
            if current_size == info.file_size:
                continue

        with open(target_file_path, "wb") as f:
            f.write(zip_obj.read(info.filename))

    for root, _, files in os.walk(target_dir):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, target_dir).replace(os.sep, "/")
            if rel_path not in zip_paths:
                os.remove(full_path)
