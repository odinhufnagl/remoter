import io
import json
import zipfile
import cloudpickle
import requests
from remoter.api.schemas import RunCodeResponse
from remoter.shared.core.result.result import Result
from remoter.shared.core.result.result_error import DefaultResultErrors

SERVER_URL = "http://localhost:8000/api/v1"


def run_code(
    zip_file: bytes, mounts: list[tuple[str, str | None]]
) -> Result[RunCodeResponse]:
    files = {"file": ("data.zip", zip_file, "application/zip")}
    data = {"mounts": json.dumps(mounts)}
    response = requests.post(SERVER_URL + "/runner/run_code", files=files, data=data)
    if response.status_code != 200:
        return Result.fail(DefaultResultErrors.unknown_error())
    response_data = response.json()

    logs = response_data.get("logs", [])
    is_error = response_data.get("is_error")
    if is_error:
        return Result.ok(
            RunCodeResponse(
                logs=logs, is_error=is_error, stderr=response_data.get("stderr")
            )
        )
    session_id = response_data.get("session_id")

    response_output = requests.get(
        SERVER_URL + f"/runner/run_code_download_output/{session_id}"
    )

    if response_output.status_code != 200:
        return Result.fail(DefaultResultErrors.unknown_error())

    content_type = response_output.headers.get("content-type")
    if content_type == "application/x-zip-compressed":
        output_zip_bytes = response_output.content

        with zipfile.ZipFile(io.BytesIO(output_zip_bytes)) as zf:
            return_value = cloudpickle.load(zf.open("response.pkl"))
            mounted_data_bytes = zf.open("mounted_data.zip").read()
        run_code_response = RunCodeResponse(
            return_value=return_value,
            mounted_data_bytes=mounted_data_bytes,
            logs=logs,
            is_error=False,
            stderr="",
        )
        return Result.ok(run_code_response)
    return Result.fail(DefaultResultErrors.unknown_error())
