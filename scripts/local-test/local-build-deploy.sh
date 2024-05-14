##### BUILD and PUSH IMAGES #####

# Fail script on errors
set -e

# REGISTRY_PW must be set as an env var before calling this script
set -u 
: "$REGISTRY_PW"

export CONTAINER_REGISTRY="ascarlat.azurecr.io"
export REGISTRY_UN="ascarlat"
export VERSION="test_2"

# Per microservice
export NAME="video-streaming"
export DIRECTORY="video-streaming"
bash ./scripts/cd/image-build.sh
bash ./scripts/cd/image-push.sh

export NAME="gateway"
export DIRECTORY="gateway"
bash ./scripts/cd/image-build.sh
bash ./scripts/cd/image-push.sh

export NAME="history"
export DIRECTORY="history"
bash ./scripts/cd/image-build.sh
bash ./scripts/cd/image-push.sh

export NAME="metadata"
export DIRECTORY="metadata"
bash ./scripts/cd/image-build.sh
bash ./scripts/cd/image-push.sh

export NAME="azure-storage"
export DIRECTORY="azure-storage"
bash ./scripts/cd/image-build.sh
bash ./scripts/cd/image-push.sh


##### DEPLOY #####
bash ./scripts/cd/deploy-infra.sh

export SERVICE_TYPE="ClusterIP"
export NAME="video-streaming"
bash ./scripts/cd/deploy-service.sh

export NAME="azure-storage"
bash ./scripts/cd/deploy-service.sh

export NAME="metadata"
bash ./scripts/cd/deploy-service.sh

export NAME="history"
bash ./scripts/cd/deploy-service.sh

export NAME="gateway"
bash ./scripts/cd/deploy-nodeport-service.sh