import sys
from timeit import default_timer as timer
from typing import Any, Callable, Tuple

from IPython import embed
from pyspark.sql import SparkSession
from pyspark.mllib import linalg
from pyspark.mllib.linalg import distributed as dist
from scipy.sparse import csc

import data


def run():
    group, name, index = parse_argv()
    csc_matrix = data.get_matrix(group, name, index)
    with get_spark_session():
        row_matrix = convert_csc_to_spark_matrix(csc_matrix)
        time_for_svd = time_call(compute_svd, row_matrix)
        print(f"SVD took {time_for_svd} seconds")


def parse_argv() -> Tuple[str, str, int]:
    group = sys.argv[1]
    name = sys.argv[2]
    index = int(sys.argv[3])
    return group, name, index


def time_call(function: Callable[[dist.RowMatrix], Any], matrix: dist.RowMatrix) -> float:
    start = timer()
    _ = function(matrix)
    end = timer()
    return end - start


def compute_svd(row_matrix: dist.RowMatrix) -> Tuple[linalg.Vector, linalg.Matrix]:
    num_singular_values = row_matrix.numCols()
    svd = row_matrix.computeSVD(num_singular_values, computeU=False)
    return svd.s, svd.V


def convert_csc_to_spark_matrix(csc_matrix: csc.csc_matrix) -> dist.RowMatrix:
    spark_session = get_spark_session()
    spark_context = spark_session.sparkContext
    matrix_as_array = csc_matrix.toarray()
    matrix_rdd = spark_context.parallelize(matrix_as_array)
    return dist.RowMatrix(matrix_rdd)


def get_spark_session() -> SparkSession:
    return SparkSession.builder.getOrCreate()


if __name__ == '__main__':
    run()
