from typing import Optional


_local_target_folder: Optional[str] = None


def set_local_target_folder(folder: str) -> None:
    global _local_target_folder
    _local_target_folder = folder


def get_local_target_folder() -> Optional[str]:
    global _local_target_folder
    return _local_target_folder
