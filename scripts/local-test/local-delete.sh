##### BUILD and PUSH IMAGES #####

# Fail script on errors
set -e

export CONTAINER_REGISTRY="ascarlat.azurecr.io"
export REGISTRY_UN="ascarlat"
export VERSION="test_1"

##### DELETE #####
kubectl delete -f ./scripts/kubernetes/rabbit.yaml
kubectl delete -f ./scripts/kubernetes/mongodb.yaml

export SERVICE_TYPE="ClusterIP"
export NAME="video-streaming"
bash ./scripts/cd/delete-service.sh

export NAME="azure-storage"
bash ./scripts/cd/delete-service.sh

export NAME="metadata"
bash ./scripts/cd/delete-service.sh

export NAME="history"
bash ./scripts/cd/delete-service.sh

export NAME="gateway"
envsubst < ./scripts/kubernetes/deploy-nodeport-service.yaml | kubectl delete -f -