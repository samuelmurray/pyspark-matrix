# pyspark-matrix
Evaluation of matrix operations using PySpark with Google Cloud Dataproc


## Example
You can run on a small matrix (85x85) locally with the following.

```
$ python3 main.py python3 HB ash85 1
```

### Cleanup
Running the above command downloads the specified matrix. To remove all downloaded files, run

```
$ make clean
```

## Create cluster
You need python3.6 on the cluster to run this. To create a cluster with python3.6 installed, run the following.

```
$ make install project=[project_id]
```

### Test your cluster
To test that your cluster has python3.6 installed correctly, you can run the following.

```
$ make test
```

## Submit job
To submit this as a job to dataproc, run the following.

```
$ make submit project=[project_id] group=HB name=ash85 index=1
```
