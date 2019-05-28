import os
import urllib.request

import numpy as np
from scipy.io import loadmat

BASE_URL = "https://sparse.tamu.edu/mat"
ENCODING = "mat"
MAT_DICT_KEY = "Problem"


def get_matrix(group: str, name: str, index: int) -> np.ndarray:
    if not os.path.isfile(name):
        download_mat(group, name)
    return _get_matrix(name, index)


def _get_matrix(name: str, index: int) -> np.ndarray:
    mat_dict = loadmat(f"{name}.{ENCODING}")
    return _get_matrix_from_mat(mat_dict, index)


def _get_matrix_from_mat(mat_dict: dict, index: int) -> np.ndarray:
    mat_array = mat_dict[MAT_DICT_KEY][0, 0]
    csc_matrix = mat_array[index]
    return csc_matrix.toarray()


def download_mat(group: str, name: str) -> None:
    url = f"{BASE_URL}/{group}/{name}.{ENCODING}"
    urllib.request.urlretrieve(url, f"{name}.{ENCODING}")
