import os
import string
import random


def find_path_of_file(desiredFile_name: str, absoluteTop: str = "C:\\"):
    for root, dirs, files in os.walk(absoluteTop):
        for name in files:
            if name == desiredFile_name:
                return os.path.abspath(os.path.join(root, name))
    raise FileNotFoundError


def create_encoder():
    while True:
        encoder = ''.join(random.choice(string.ascii_uppercase + string.digits,
                          k=32))

        try:
            find_path_of_file(encoder)
        except FileNotFoundError:
            break

    return encoder
