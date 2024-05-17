Dev notes
---------

Todo
----
* Have the upload service publish a "videoUploaded" message via the bus and remove the code
  that saves the video to the videos collection.
  - Then have the storage service query the storage when it first boots up and send messages about videos
    that it finds there.
  - Metadata service picks up these messages and if the video doesn't exist save it to the videos collection.

* (DONE) Split the build stage into multiple yaml files with the `path` attribute so that they run only when code
  gets checked into their folders.
  - It's not just the build pipeline, each of these files will also have the deployment code for that 
    microservice. 
  - They will still use the templates

* In the history server, do the count views aggregation using mongodb (and not in python).

* (DONE) Move common code to pypi packages

Docs
----
* Pika aio and fastapi set up
  - https://itracer.medium.com/rabbitmq-publisher-and-consumer-with-fastapi-175fe87aefe1
  - https://aio-pika.readthedocs.io/en/latest/rabbitmq-tutorial/3-publish-subscribe.html

* Pytest
  - https://docs.pytest.org/en/latest/explanation/goodpractices.html#choosing-a-test-layout-import-rules

Docker
------
* Build for linux/amd64 (required when building and pushing from M2 Mac):
```bash
docker build -f  ./dockerfile-prod --platform=linux/amd64  -t video-streaming:2 .
```

Azure K8S
---------
* Build the cluster using tf:

```bash
cd ./scripts/terraform
bash -x tf_apply.sh
```

* Cluster specs:
  - Worker node pool
    * B2
  - System node pool
    * Standard_D2s_v3

* Set up kube context:
```bash
az aks get-credentials --resource-group ascarlat_learning --name ascarlat
```

* (NOT NEEDED) Attach the container registry to the cluster (not needed if configured via tf):
```bash
az aks update --resource-group ascarlat_learning --name ascarlat --attach-acr ascarlat
```

* Create the global-config map:
```bash
kubectl create configmap global-env --from-env-file=.env
```

* Deploy cluster from local machine:
  - Run the above steps to set up the cluster
  - Run: 
``` bash
bash -x scripts/local-test/local-build-deploy.sh

# Once cluster is running
kubectl port-forward service/gateway 30000:80  
```
  

Github Actions
--------------
* Making a script executable before pushing it to git:

```bash
git update-index --chmod=+x hello.sh
```

* `KUBE_CONFIG` must be set up as an actions secret (different per cluster)
  - The image registry secrets should also be set but those dont change
  - To add the kube_config to the secrets, first base64 it, then add it as a secret:

```bash
cat ~/.kube/config | base64 > kube_tmp
```

