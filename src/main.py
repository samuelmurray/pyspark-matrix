import os
import sys
from typing import Tuple

import data
import matrix


def run():
    group, name, index = parse_argv()
    np_matrix = data.get_matrix(group, name, index)
    matrix.run_operations_on_matrix(np_matrix)


def parse_argv() -> Tuple[str, str, int]:
    os.environ["PYSPARK_PYTHON"] = sys.argv[1]
    group = sys.argv[2]
    name = sys.argv[3]
    index = int(sys.argv[4])
    return group, name, index


if __name__ == '__main__':
    run()
