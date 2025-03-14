def return_file(file_path):
    global response_file_paths
    if "response_file_paths" not in globals():
        response_file_paths = []
    response_file_paths.append(file_path)
