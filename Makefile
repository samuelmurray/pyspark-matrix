.PHONY: default submit clean

default:
	@ echo Run \"make clean\" to remove all downloaded files

submit:
	gcloud dataproc jobs submit pyspark gs://${PROJECT_ID}/main.py \
		--py-files "gs://${PROJECT_ID}/matrix.py,gs://${PROJECT_ID}/data.py" \
		--cluster=conda-cluster \
		--properties "spark.pyspark.python=python3.6,spark.pyspark.driver.python=python3.6" \
		-- /opt/conda/bin/python3.6 ${group} ${name} ${index}

clean:
	rm -fv *.mat
