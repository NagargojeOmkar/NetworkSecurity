import os
import sys
import yaml
import pickle
import numpy as np

from networksecurity.exception.exception import NetworkSecurityException


# ==============================
# READ YAML FILE
# ==============================
def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "r") as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)


# ==============================
# WRITE YAML FILE
# ==============================
def write_yaml_file(file_path: str, content: dict):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)


# ==============================
# SAVE NUMPY ARRAY
# ==============================
def save_numpy_array_data(file_path: str, array: np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)

    except Exception as e:
        raise NetworkSecurityException(e, sys)


# ==============================
# SAVE OBJECT (MODEL / PIPELINE)
# ==============================
def save_object(file_path: str, obj: object) -> None:
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise NetworkSecurityException(e, sys)