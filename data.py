import os
import urllib.request

from scipy.io import loadmat
from scipy.sparse import csc

BASE_URL = "https://sparse.tamu.edu/mat"
ENCODING = "mat"
MAT_DICT_KEY = "Problem"


def get_matrix(group: str, name: str, index: int) -> csc.csc_matrix:
    if not os.path.isfile(name):
        download_mat(group, name)
    return _get_matrix(name, index)


def _get_matrix(name: str, index: int) -> csc.csc_matrix:
    mat_dict = loadmat(f"{name}.{ENCODING}")
    return _get_matrix_from_mat(mat_dict, index)


def _get_matrix_from_mat(mat_dict: dict, index: int):
    array = mat_dict[MAT_DICT_KEY][0, 0]
    return array[index]


def download_mat(group: str, name: str) -> None:
    url = f"{BASE_URL}/{group}/{name}.{ENCODING}"
    urllib.request.urlretrieve(url, f"{name}.{ENCODING}")
