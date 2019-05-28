import sys
from typing import Tuple

import data
import matrix


def run():
    group, name, index = parse_argv()
    np_matrix = data.get_matrix(group, name, index)
    matrix.run_operations_on_matrix(np_matrix)


def parse_argv() -> Tuple[str, str, int]:
    group = sys.argv[1]
    name = sys.argv[2]
    index = int(sys.argv[3])
    return group, name, index


if __name__ == '__main__':
    run()