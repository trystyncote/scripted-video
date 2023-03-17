import os
import string
import random


def find_file(start_dir, filename):
    for root, dirs, files in os.walk(start_dir):
        if filename in files:
            return os.path.join(root, filename)
    return None


def find_path_of_file(filename):
    current_dir = os.path.abspath('.')
    while True:
        file_path = find_file(current_dir, filename)
        if file_path:
            return file_path
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:
            raise FileNotFoundError
        current_dir = parent_dir


def create_encoder():
    while True:
        encoder = ''.join(random.choices(string.ascii_uppercase + string.digits,
                          k=32))

        try:
            find_path_of_file(encoder)
        except FileNotFoundError:
            break

    return encoder
