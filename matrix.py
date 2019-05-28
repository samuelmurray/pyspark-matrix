from timeit import default_timer as timer
from typing import Any, Callable, Tuple

from pyspark import SparkContext
from pyspark.mllib import linalg
from pyspark.mllib.linalg import distributed as dist
from pyspark.sql import SparkSession
from scipy.sparse import csc


def run_operations_on_matrix(csc_matrix: csc.csc_matrix) -> None:
    with get_spark_session():
        row_matrix = convert_csc_to_spark_matrix(csc_matrix)
        time_for_svd = time_call(compute_svd, row_matrix)
        print(f"SVD took {time_for_svd} seconds")


def convert_csc_to_spark_matrix(csc_matrix: csc.csc_matrix) -> dist.RowMatrix:
    spark_context = get_spark_context()
    matrix_as_array = csc_matrix.toarray()
    matrix_rdd = spark_context.parallelize(matrix_as_array)
    return dist.RowMatrix(matrix_rdd)


def time_call(function: Callable[[dist.RowMatrix], Any], matrix: dist.RowMatrix) -> float:
    start = timer()
    _ = function(matrix)
    end = timer()
    return end - start


def compute_svd(row_matrix: dist.RowMatrix) -> Tuple[linalg.Vector, linalg.Matrix]:
    num_singular_values = row_matrix.numCols()
    svd = row_matrix.computeSVD(num_singular_values, computeU=False)
    return svd.s, svd.V


def get_spark_session() -> SparkSession:
    return SparkSession.builder.getOrCreate()


def get_spark_context() -> SparkContext:
    session = get_spark_session()
    return session.sparkContext
