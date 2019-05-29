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
$ make install project=[your_project_id]
```

### Test your cluster
To test that your cluster has python3.6 installed correctly, you can run the following.

```
$ make test
```

## Submit job
To submit this as a job to dataproc, run the following.

```
$ project="[your_project_id]"
$ gcloud dataproc jobs submit pyspark gs://${project}/main.py \
--py-files "gs://${project}/matrix.py,gs://${project}/data.py" \
--cluster=conda-cluster \
--properties "spark.pyspark.python=python3.6,spark.pyspark.driver.python=python3.6" \
-- /opt/conda/bin/python3.6 HB ash85 1
```

### Makefile
You can also use the provided Makefile to submit jobs. The equivalent call as above would be

```
$ make submit project=[your_project_id] group=HB name=ash85 index=1
```
