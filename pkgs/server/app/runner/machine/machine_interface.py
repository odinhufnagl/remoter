import json
import os
import re
import shutil
import subprocess
from sys import stderr
from typing import Any
import zipfile

import cloudpickle
from pydantic import BaseModel
from requests import session
from sqlmodel import extract

from app.runner.machine.machine_errors import MachineError, MachineErrors
from app.shared.core.result.result import Result


MACHINE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "DOCKER_MACHINE"
)


class MachineRunResponse(BaseModel):
    output_dir: str
    logs: str
    image_name: str
    session_id: str
    is_error: bool
    stderr: str


def docker_cmd_run_container(image_name, session_path):
    docker_cmd = [
        "docker",
        "run",
        "--rm",
        "-v",
        f"{os.path.abspath(session_path)}:/app/tmp/session",
        "-v",
        f"{os.path.join(os.path.abspath(session_path), "machine_dir")}:/app/fake_run",
        image_name,
    ]
    return docker_cmd


def docker_cmd_rm_image(image_name):
    docker_cmd = [
        "docker",
        "image",
        "rm",
        image_name,
    ]
    return docker_cmd


def docker_cmd_prune_volumes():
    docker_cmd = [
        "docker",
        "volume",
        "prune",
        "-f",
    ]
    return docker_cmd


def docker_cmd_build_image(image_name, build_context):
    docker_cmd = [
        "docker",
        "build",
        "-t",
        image_name,
        "-f",
        build_context + "/Dockerfile",
        "--build-arg",
        f"REQUIREMENTS_FILE=requirements.txt",
        build_context,
    ]
    return docker_cmd


def build_and_run_docker_file(
    image_name,
    tmp_path,
    build_context,
    mounts: list[tuple[str, str | None]],
    session_id: str,
) -> Result[MachineRunResponse, MachineError]:
    session_path = tmp_path
    os.makedirs(os.path.join(session_path, "machine_dir"), exist_ok=True)
    requirements_path = os.path.join(tmp_path, "input", "requirements.txt")
    print("huhuyhuyh", os.listdir(os.path.join(tmp_path, "input", "mounted_data")))
    shutil.copy(requirements_path, build_context)
    try:
        subprocess.run(docker_cmd_build_image(image_name, build_context))
    except:
        return Result[MachineRunResponse, MachineError].fail(
            MachineErrors.build_error()
        )
    try:
        print("listdir", os.listdir(session_path))
        run_result = subprocess.run(
            docker_cmd_run_container(image_name, session_path),
            capture_output=True,
            text=True,
        )
        print("heyyy", run_result)
        print("responseeee", os.listdir(os.path.join(tmp_path, "output")))
    except:
        return Result[MachineRunResponse, MachineError].fail(MachineErrors.run_error())
    subprocess.run(docker_cmd_rm_image(image_name), check=True)
    subprocess.run(docker_cmd_prune_volumes(), check=True)
    output_dir = os.path.join(tmp_path, "output")

    mounted_output_dir = os.path.join(output_dir, "mounted_data")
    for mount_client_path, mount_path in mounts:
        mount_path = mount_path or mount_client_path
        shutil.make_archive(
            os.path.join(mounted_output_dir, mount_client_path),
            "zip",
            os.path.join(session_path, "machine_dir", mount_path),
        )

    shutil.make_archive(mounted_output_dir, "zip", mounted_output_dir)
    shutil.rmtree(mounted_output_dir)
    output_zip_path = shutil.make_archive(output_dir, "zip", output_dir)
    response_value_path = os.path.join(output_dir, "response.pkl")
    response = MachineRunResponse(
        output_dir=output_zip_path,
        logs=run_result.stdout,
        stderr=run_result.stderr,
        image_name=image_name,
        session_id=session_id,
        is_error=run_result.stderr != "",
    )
    return Result[MachineRunResponse, MachineError].ok(response)


def build_and_run_machine(
    tmp_path, session_id, mounts: list[tuple[str, str | None]]
) -> Result[MachineRunResponse]:
    build_context = MACHINE_PATH
    print("buuuuu", build_context)
    image_name = f"machine.{session_id}"
    return build_and_run_docker_file(
        image_name, tmp_path, build_context, mounts, session_id
    )
