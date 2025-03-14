_mount_folder_paths: list[tuple[str, str | None]] = []
_upload_folder_paths: list[tuple[str, str]] = []


def mount_folder(path, remote_path):
    global _mount_folder_paths
    _mount_folder_paths.append((path, remote_path))


def get_mount_folder_paths() -> list[tuple[str, str | None]]:
    global _mount_folder_paths
    return _mount_folder_paths


def upload_folder(path, remote_path):
    global _upload_folder_paths
    _upload_folder_paths.append((path, remote_path))


def get_upload_folder_paths() -> list[tuple[str, str]]:
    global _upload_folder_paths
    return _upload_folder_paths
