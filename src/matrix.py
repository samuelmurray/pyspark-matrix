from timeit import default_timer as timer
from typing import Any, Callable, Tuple

import numpy as np
from pyspark import SparkContext
from pyspark.mllib import linalg
from pyspark.mllib.linalg import distributed as dist
from pyspark.sql import SparkSession


def run_operations_on_matrix(np_matrix: np.ndarray) -> None:
    with get_spark_session() as session:
        row_matrix = create_spark_matrix(np_matrix, session)
        repeats = 10
        functions = [singular_value_decomposition, qr_decomposition]
        for function in functions:
            time = time_function_call(function, row_matrix, repeats)
            print_time_for_function(function, time, repeats)


def create_spark_matrix(np_matrix: np.ndarray, session: SparkSession) -> dist.RowMatrix:
    spark_context = get_spark_context(session)
    matrix_rdd = spark_context.parallelize(np_matrix)
    return dist.RowMatrix(matrix_rdd)


def time_function_call(function: Callable[[dist.RowMatrix], Any], matrix: dist.RowMatrix,
                       repeats: int) -> float:
    start = timer()
    for i in range(repeats):
        _ = function(matrix)
    end = timer()
    return end - start


def singular_value_decomposition(matrix: dist.RowMatrix) -> Tuple[linalg.Vector, linalg.Matrix]:
    num_singular_values = matrix.numCols()
    decomposition = matrix.computeSVD(num_singular_values, computeU=False)
    return decomposition.s, decomposition.V


def qr_decomposition(matrix: dist.RowMatrix) -> linalg.Matrix:
    decomposition = matrix.tallSkinnyQR()
    return decomposition.R


def print_time_for_function(function: callable, time: float, repeats: int) -> None:
    print(f"Running {function.__name__} {repeats} times took {time} seconds, "
          f"for an average of {time / repeats} seconds")


def get_spark_session() -> SparkSession:
    return SparkSession.builder.getOrCreate()


def get_spark_context(session: SparkSession) -> SparkContext:
    return session.sparkContext
