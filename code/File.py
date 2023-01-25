import os


def find_path_of_file(desiredFile_name: str, absoluteTop: str = "C:\\"):
    for root, dirs, files in os.walk(absoluteTop):
        for name in files:
            if name == desiredFile_name:
                return os.path.abspath(os.path.join(root, name))
