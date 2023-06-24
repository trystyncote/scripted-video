from pathlib import Path
import random
import string


def _recurse_search_child_directory(desired_file_name: str, current_directory: Path):
    try:
        for child_path in current_directory.iterdir():
            if child_path.is_dir():
                return_context = _recurse_search_child_directory(desired_file_name, child_path)
                if return_context:
                    return return_context
            elif child_path.is_file() and child_path.name == desired_file_name:
                return child_path
    except PermissionError:
        pass
    return None


def find_path_of_file(desired_file_name: str):
    complete_directory = Path(".").absolute()
    current_directory = complete_directory

    while (current_directory := current_directory.parent) != complete_directory.parents[-1]:
        return_context = _recurse_search_child_directory(desired_file_name, current_directory)
        if return_context:
            return return_context
    raise FileNotFoundError


def create_encoder():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=32))
