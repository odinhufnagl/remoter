import io
import json
import os
import subprocess
import tempfile
import zipfile
import cloudpickle
from typing import Callable, Any, TypeVar
import sys

import os
import shutil
import tempfile


from remoter.api import api
from remoter.runner.local_target_folder import get_local_target_folder
from remoter.runner.mounting import get_mount_folder_paths
from remoter.runner.requirements_config import get_requirements
from remoter.runner.response import RunResponse
from remoter.runner.response_collector import ResponseCollector
from remoter.shared.utils import (
    add_folder_to_zip,
    add_folders_in_new_folder_in_zipfile,
    sync_folder_with_zip,
)

ResponseType = TypeVar("ResponseType")
FuncType = Callable[..., ResponseType]


def filter_sys_path():
    # Example filtering: remove paths that contain common system directories.
    system_paths = [
        os.path.dirname(sys.executable),
        "/usr/lib",
        "/usr/local/lib",
    ]
    filtered = []
    for p in sys.path:
        if not any(sp in p for sp in system_paths):
            filtered.append(p)
    return [sys.path[0]]
    # return filtered


def serialize_function(wrapped_func) -> str:
    with tempfile.NamedTemporaryFile(suffix=".pkl", delete=False) as tmp:
        cloudpickle.dump(wrapped_func, tmp)
        tmp_path = tmp.name
    return tmp_path


def package_server_data(
    wrapped_func,
    sys_paths: list[str],
    requirements_path: str | None,
    mount_folder_paths: list[tuple[str, str | None]],
) -> bytes:
    function_tmp_path = serialize_function(wrapped_func)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:

        zipf.write(function_tmp_path, arcname="function.pkl")

        add_folders_in_new_folder_in_zipfile(
            zipf, sys_paths, target_folder_name="sys_paths"
        )
        if requirements_path:
            zipf.write(requirements_path, arcname="requirements.txt")
        if len(mount_folder_paths):
            for path, remote_path in mount_folder_paths:
                add_folder_to_zip(
                    zipf,
                    path,
                    os.path.join("mounted_data", remote_path or path),
                )

    zip_buffer.seek(0)

    os.remove(function_tmp_path)

    return zip_buffer.getvalue()


def run(func: FuncType, *args: Any, **kwargs: Any) -> Any:
    print("Running")

    def wrapped_func():
        return func(*args, **kwargs)

    requirements = get_requirements()
    mount_folder_paths = get_mount_folder_paths()
    print("mount_folder_paths", mount_folder_paths)
    sys_paths = filter_sys_path()
    zipped_server_data = package_server_data(
        wrapped_func, sys_paths, requirements, mount_folder_paths
    )
    print("huhuhuh")
    response = api.run_code(zipped_server_data, mount_folder_paths)
    print("babab")
    if response.is_failure():
        raise response.error.exc()
    res = response.get_value()
    if res.logs is not None and res.logs != "":
        print("Logs:", res.logs)
    if res.is_error:
        print("Error:", res.stderr)
        return
    if not res.mounted_data_bytes:
        return res.return_value
    with zipfile.ZipFile(io.BytesIO(res.mounted_data_bytes)) as outer_zip:
        for mount_path, _ in mount_folder_paths:
            os.makedirs(mount_path, exist_ok=True)
            mount_bytes = outer_zip.read(mount_path + ".zip")
            with zipfile.ZipFile(io.BytesIO(mount_bytes)) as inner_zip:
                sync_folder_with_zip(inner_zip, mount_path)

    return res.return_value
    """ extracted_return_value = return_value.return_value
    client_directory = os.getcwd()
    local_target = get_local_target_folder() or "extracted"
    print("local_target", local_target)
    extract_path = os.path.join(client_directory, local_target)
    with zipfile.ZipFile(io.BytesIO(res.files_zip_bytes)) as zf:
        zf.extractall(path=extract_path)
        print(f"Extracted files: {zf.namelist()} to {extract_path}")

    return extracted_return_value"""


def mount():
    pass
