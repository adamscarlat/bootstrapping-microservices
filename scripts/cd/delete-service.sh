# 
# Remove containers from Kubernetes.
#
# Environment variables:
#
#   NAME - The name of the microservice to delete.
#
# Usage:
#
#   ./scripts/cd/delete.sh
#
set -u # or set -o nounset
: "$NAME"

envsubst < ./scripts/kubernetes/deploy-service.yaml | kubectl delete -f -