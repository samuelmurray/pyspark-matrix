import os
import urllib.request

from scipy.io import loadmat
from scipy.sparse import csc

BASE_URL = "https://sparse.tamu.edu/mat"
ENCODING = "mat"


def get_matrix(group: str, name: str, index: int) -> csc.csc_matrix:
    if not os.path.isfile(name):
        download_mat(group, name)
    mat_dict = get_mat(name)
    return get_matrix_from_dict(mat_dict, index)


def get_matrix_from_dict(mat_dict, index) -> csc.csc_matrix:
    array = mat_dict["Problem"][0, 0]
    csc_matrix = array[index]
    return csc_matrix


def get_mat(name: str) -> dict:
    return loadmat(f"{name}.{ENCODING}")


def download_mat(group: str, name: str) -> None:
    url = f"{BASE_URL}/{group}/{name}.{ENCODING}"
    urllib.request.urlretrieve(url, f"{name}.{ENCODING}")
