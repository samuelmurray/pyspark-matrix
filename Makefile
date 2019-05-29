.PHONY: default submit test clean

default:
	@ echo Run \"make clean\" to remove all downloaded files

submit:
	gcloud dataproc jobs submit pyspark gs://${project}/main.py \
		--py-files "gs://${project}/matrix.py,gs://${project}/data.py" \
		--cluster=conda-cluster \
		--properties "spark.pyspark.python=python3.6,spark.pyspark.driver.python=python3.6" \
		-- /opt/conda/bin/python3.6 ${group} ${name} ${index}

test:
	gcloud dataproc jobs submit pyspark check_python_env.py \
		--cluster=conda-cluster \
		--properties "spark.pyspark.python=python3.6,spark.pyspark.driver.python=python3.6"

clean:
	rm -fv *.mat
