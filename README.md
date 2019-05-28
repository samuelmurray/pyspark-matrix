# pyspark-matrix
Evaluation of matrix operations using PySpark with Google Cloud Dataproc


## Example
You can run on a small matrix (85x85) with the following:

```
$ python3 main.py HB ash85 1
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
