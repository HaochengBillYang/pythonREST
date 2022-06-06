## use to delete all files under /__pycache__/, prevent git conflict
import os


def remove_all(path: str):
    files = os.listdir(path)
    for file in files:
        if file == ".." or file == ".":
            continue
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path) and file_path.endswith(".pyc"):
            print("delete: " + file_path)
            os.remove(file_path)


def run(path: str):
    files = os.listdir(path)
    for file in files:
        if file == ".." or file == ".":
            continue
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            if file == "__pycache__":
                remove_all(file_path)
            else:
                run(file_path)


run(os.path.dirname(__file__))
