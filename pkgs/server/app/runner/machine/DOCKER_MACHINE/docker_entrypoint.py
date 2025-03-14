import base64
import io
import json
import shutil
import sys
import os
import zipfile
import cloudpickle
from contextlib import redirect_stdout, redirect_stderr

"""def extract_function_result_to_output(func_result, output_path):
    print("1", type(func_result))
    if isinstance(func_result, ResponseCollector):
        file_paths = func_result.file_paths
        # zip the files
        zip_file_path = os.path.join(output_path, "response_files.zip")
        with zipfile.ZipFile(zip_file_path, "w") as zipf:
            for remote_file_path, client_local_file_path in file_paths:
                zipf.write(remote_file_path, client_local_file_path or remote_file_path)
"""


def move_dir_contents(source_dir, target_dir):
    os.makedirs(target_dir, exist_ok=True)
    for item in os.listdir(source_dir):
        s = os.path.join(source_dir, item)
        d = os.path.join(target_dir, item)
        shutil.move(s, d)


def main():
    session_path = os.path.abspath("./tmp/session")
    input_path = os.path.join(session_path, "input")
    output_path = os.path.join(session_path, "output")
    input_mounted_data_path = os.path.join(input_path, "mounted_data")
    move_dir_contents(input_mounted_data_path, "./fake_run")
    with open(os.path.join(input_path, "function.pkl"), "rb") as f:
        func = cloudpickle.load(f)
    session_sys_paths = os.path.join(input_path, "sys_paths")
    sys.path = [session_sys_paths] + sys.path

    func_result_value_path = os.path.join(output_path, "response.pkl")
    os.chdir("./fake_run")
    log_stream = io.StringIO()
    with redirect_stdout(log_stream), redirect_stderr(log_stream):
        func_result = func()  # Execute the function; logs will be captured.

    # Retrieve the captured logs.
    logs = log_stream.getvalue()
    print(logs)
    # extract_function_result_to_output(func_result, output_path)
    with open(func_result_value_path, "wb") as f:
        cloudpickle.dump(func_result, f)


if __name__ == "__main__":
    main()
