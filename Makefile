.PHONY: default install submit test clean

default:
	@ echo Run \"make clean\" to remove all downloaded files

submit:
	gcloud dataproc jobs submit pyspark gs://${project}/main.py \
		--py-files "gs://${project}/matrix.py,gs://${project}/data.py" \
		--cluster=conda-cluster \
		--properties "spark.pyspark.python=python3.6,spark.pyspark.driver.python=python3.6" \
		-- /opt/conda/bin/python3.6 ${group} ${name} ${index}

install:
	gcloud dataproc clusters create conda-cluster \
		--metadata 'CONDA_PACKAGES="numpy scipy"' \
		--initialization-actions gs://dataproc-initialization-actions/conda/bootstrap-conda.sh,gs://dataproc-initialization-actions/conda/install-conda-env.sh \
		--project=${project} \
		--worker-machine-type='n1-standard-2'

test:
	gcloud dataproc jobs submit pyspark check_python_env.py \
		--cluster=conda-cluster \
		--properties "spark.pyspark.python=python3.6,spark.pyspark.driver.python=python3.6"

clean:
	rm -fv *.mat
