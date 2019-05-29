.PHONY: default install test submit clean

default:
	@ echo -e "Run  \"make install project=[project_id]\" to setup a cluster \n\
		\"make test\" to test the cluster \n\
		\"make submit project=[project_id] group=[matrix_group] name=[name] index=[index]\" to submit a job \n\
		\"make clean\" to remove all downloaded files"

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

submit:
	gcloud dataproc jobs submit pyspark gs://${project}/main.py \
		--py-files "gs://${project}/matrix.py,gs://${project}/data.py" \
		--cluster=conda-cluster \
		--properties "spark.pyspark.python=python3.6,spark.pyspark.driver.python=python3.6" \
		-- /opt/conda/bin/python3.6 ${group} ${name} ${index}

clean:
	rm -fv *.mat
