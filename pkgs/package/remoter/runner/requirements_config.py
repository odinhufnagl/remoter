_requirements_path = None


def set_requirements(file_path: str):
    global _requirements_path
    _requirements_path = file_path


def get_requirements():
    global _requirements_path
    return _requirements_path
