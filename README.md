Dev notes
---------
* Book: 8.7.4

Temp
----
* viewed video message:

```json
{
"id":2,
"video_path":"hey1"
}
```

Docs
----
* Pika aio and fastapi set up
  - https://itracer.medium.com/rabbitmq-publisher-and-consumer-with-fastapi-175fe87aefe1
  - https://aio-pika.readthedocs.io/en/latest/rabbitmq-tutorial/3-publish-subscribe.html

Docker
------
* Build for linux/amd64 (required when building and pushing from M2 Mac):
```bash
docker build -f  ./dockerfile-prod --platform=linux/amd64  -t video-streaming:2 .
```

Azure K8S
---------
* Cluster specs:
  - Worker node pool
    * B2
  - System node pool
    * Standard_D2s_v3

* Set up kube context:
```bash
az aks get-credentials --resource-group ascarlat_learning --name ascarlat
```

* Attach the container registry to the cluster:
```bash
az aks update --resource-group ascarlat_learning --name ascarlat --attach-acr ascarlat
```

* Create the global-config map:
```bash
kubectl create configmap global-env --from-env-file=.env
```
