# pyspark-matrix
Evaluation of matrix operations using PySpark with Google Cloud Dataproc


## Example
You can run on a small matrix (85x85) locally with the following.

```
$ python3 main.py python3 HB ash85 1
```


## Create cluster
You need python3.6 on the cluster to run this. To create a cluster with python3.6 installed, run the following.

```
$ export PROJECT_ID=[your_project_id]
$ gcloud dataproc clusters create conda-cluster \
--metadata 'CONDA_PACKAGES="numpy scipy"' \
--initialization-actions gs://dataproc-initialization-actions/conda/bootstrap-conda.sh,gs://dataproc-initialization-actions/conda/install-conda-env.sh \
--project=${PROJECT_ID} \
--worker-machine-type='n1-standard-2' 
```

### Test your cluster
To test that your cluster has python3.6 installed correctly, you can run the following.

```
$ gcloud dataproc jobs submit pyspark check_python_env.py \
--cluster=conda-cluster \
--properties "spark.pyspark.python=python3.6,spark.pyspark.driver.python=python3.6"
```

## Submit job
To submit this as a job to dataproc, run the following.

```
$ export PROJECT_ID="[your_project_id]"
$ gcloud dataproc jobs submit pyspark gs://${PROJECT_ID}/main.py \
--py-files "gs://${PROJECT_ID}/matrix.py,gs://${PROJECT_ID}/data.py" \
--cluster=conda-cluster \
--properties "spark.pyspark.python=python3.6,spark.pyspark.driver.python=python3.6" \
-- /opt/conda/bin/python3.6 HB ash85 1
```
