import sys
from timeit import default_timer as timer
from typing import Tuple

from IPython import embed
from pyspark.sql import SparkSession
from pyspark.mllib import linalg
from pyspark.mllib.linalg import distributed as dist
from scipy.sparse import csc

import data


def run():
    group, name, index = parse_argv()
    csc_matrix = data.get_matrix(group, name, index)
    spark = SparkSession.builder.getOrCreate()
    row_matrix = convert_csc_to_spark_matrix(spark, csc_matrix)
    time_for_svd = time_call(compute_svd, row_matrix)
    print(f"SVD took {time_for_svd} seconds")
    spark.stop()


def parse_argv():
    group = sys.argv[1]
    name = sys.argv[2]
    index = int(sys.argv[3])
    return group, name, index


def time_call(function: callable, matrix: dist.RowMatrix) -> float:
    start = timer()
    _ = function(matrix)
    end = timer()
    return end - start


def compute_svd(row_matrix: dist.RowMatrix) -> Tuple[linalg.Vector, linalg.Matrix]:
    num_singular_values = row_matrix.numCols()
    svd = row_matrix.computeSVD(num_singular_values, computeU=False)
    return svd.s, svd.V


def convert_csc_to_spark_matrix(spark_session: SparkSession,
                                csc_matrix: csc.csc_matrix) -> dist.RowMatrix:
    matrix_as_array = csc_matrix.toarray()
    spark_context = spark_session.sparkContext
    matrix_rdd = spark_context.parallelize(matrix_as_array)
    return dist.RowMatrix(matrix_rdd)


if __name__ == '__main__':
    run()
