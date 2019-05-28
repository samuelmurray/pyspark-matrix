import os
import urllib.request

from scipy.io import loadmat

BASE_URL = "https://sparse.tamu.edu/mat"
ENCODING = "mat"


def get_mat(group: str, name: str) -> dict:
    if not os.path.isfile(name):
        download_mat(group, name)
    return loadmat(f"{name}.{ENCODING}")


def download_mat(group: str, name: str) -> None:
    url = f"{BASE_URL}/{group}/{name}.{ENCODING}"
    urllib.request.urlretrieve(url, f"{name}.{ENCODING}")
