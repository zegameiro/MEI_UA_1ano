#!/bin/bash
set -e

# Configurações
REGISTRY="registry.deti"
NAMESPACE="g11-bytebazaar"

# Imagens personalizadas
FRONTEND_IMAGE="g11-bytebazaar/ecom-frontend"
BACKEND_IMAGE="g11-bytebazaar/ecom-backend"
BUDIBASE_IMAGE="g11-bytebazaar/ecom-budibase"
UPLOAD_IMAGE="g11-bytebazaar/ecom-upload-server"

# Flags globais
BUILD_IMAGES=false
PUSH_IMAGES=false
DELETE_ALL_DEPLOYMENTS=false

# Flags de deploy
DEPLOY_FRONTEND=false
DEPLOY_BACKEND=false
DEPLOY_UPLOAD=false
DEPLOY_MYSQL=false
DEPLOY_REDIS=false
DEPLOY_BUDIBASE=false
DEPLOY_INGRESS=false
DEPLOY_GRAFANA=false
DEPLOY_JAEGER=false
DEPLOY_PROMETHEUS=false
DEPLOY_OTEL=false
DEPLOY_CONFIGMAP=false
DEPLOY_PVC_OBSERVABILITY=false

# Flags de delete individual
DELETE_FRONTEND=false
DELETE_BACKEND=false
DELETE_UPLOAD=false
DELETE_MYSQL=false
DELETE_REDIS=false
DELETE_BUDIBASE=false
DELETE_INGRESS=false
DELETE_GRAFANA=false
DELETE_JAEGER=false
DELETE_PROMETHEUS=false
DELETE_OTEL=false
DELETE_CONFIGMAP=false
DELETE_PVC_OBSERVABILITY=false

# Parse de argumentos
while [[ $# -gt 0 ]]; do
  case "$1" in
    --build) BUILD_IMAGES=true ;;
    --push) PUSH_IMAGES=true ;;
    --delete_all) DELETE_ALL_DEPLOYMENTS=true ;;
    --frontend) DEPLOY_FRONTEND=true ;;
    --backend) DEPLOY_BACKEND=true ;;
    --upload) DEPLOY_UPLOAD=true ;;
    --mysql) DEPLOY_MYSQL=true ;;
    --redis) DEPLOY_REDIS=true ;;
    --budibase) DEPLOY_BUDIBASE=true ;;
    --ingress) DEPLOY_INGRESS=true ;;
    --grafana) DEPLOY_GRAFANA=true ;;
    --jaeger) DEPLOY_JAEGER=true ;;
    --prometheus) DEPLOY_PROMETHEUS=true ;;
    --otel) DEPLOY_OTEL=true ;;
    --configmap) DEPLOY_CONFIGMAP=true ;;
    --pvc_observability) DEPLOY_PVC_OBSERVABILITY=true ;;
    --delete-frontend) DELETE_FRONTEND=true ;;
    --delete-backend) DELETE_BACKEND=true ;;
    --delete-upload) DELETE_UPLOAD=true ;;
    --delete-mysql) DELETE_MYSQL=true ;;
    --delete-redis) DELETE_REDIS=true ;;
    --delete-budibase) DELETE_BUDIBASE=true ;;
    --delete-ingress) DELETE_INGRESS=true ;;
    --delete-grafana) DELETE_GRAFANA=true ;;
    --delete-jaeger) DELETE_JAEGER=true ;;
    --delete-prometheus) DELETE_PROMETHEUS=true ;;
    --delete-otel) DELETE_OTEL=true ;;
    --delete-configmap) DELETE_CONFIGMAP=true ;;
    --delete-pvc_observability) DELETE_PVC_OBSERVABILITY=true ;;
    --all)
      DEPLOY_FRONTEND=true
      DEPLOY_BACKEND=true
      DEPLOY_UPLOAD=true
      DEPLOY_MYSQL=true
      DEPLOY_REDIS=true
      DEPLOY_BUDIBASE=true
      DEPLOY_INGRESS=true
      DEPLOY_GRAFANA=true
      DEPLOY_JAEGER=true
      DEPLOY_PROMETHEUS=true
      DEPLOY_OTEL=true
      DEPLOY_CONFIGMAP=true
      DEPLOY_PVC_OBSERVABILITY=true
      ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
  shift
done

# Commit hash
COMMIT_HASH=$(git rev-parse --short HEAD)
echo "Deploy Version: $COMMIT_HASH"

# Função para deletar componente
delete_component() {
  local folder=$1
  local base="./k3s/$folder"

  echo "Deleting $folder..."

  case "$folder" in
    mysql)
      kubectl delete -f "$base/configmap.yaml" -n $NAMESPACE
      kubectl delete -f "$base/statefulset.yaml" -n $NAMESPACE
      kubectl delete -f "$base/secrets.yml" -n $NAMESPACE
      ;;
    redis)
      kubectl delete -f "$base/statefulset_sentinel.yaml" -n $NAMESPACE
      kubectl delete -f "$base/statefulset.yaml" -n $NAMESPACE
      ;;
    backend)
      kubectl delete -f "$base/hpa.yaml" -n $NAMESPACE
      kubectl delete -f "$base/deployment.yaml" -n $NAMESPACE
      kubectl delete -f "$base/secrets.yml" -n $NAMESPACE
      ;;
    client)
      kubectl delete -f "$base/hpa.yaml" -n $NAMESPACE
      kubectl delete -f "$base/deployment.yaml" -n $NAMESPACE
      ;;
    upload-server|budibase|ingress)
      for file in "$base"/*.yaml; do
        [ -f "$file" ] && kubectl delete -f "$file" -n $NAMESPACE
      done
      ;;
    grafana|jaeger|prometheus|otel-collector|configmap|pvc_observability)
      for file in "./k3s/$folder"/*.yaml; do
        [ -f "$file" ] && kubectl delete -f "$file" -n $NAMESPACE
      done
      ;;
    *)
      echo "Unknown component folder: $folder"
      ;;
  esac
}

# Função para aplicar componente e setar imagem (se aplicável)
apply_component() {
  local folder=$1
  local deployment_name=$2
  local image=$3
  local container_name=$4
  local base="./k3s/$folder"

  echo "Applying $name..."  

  case "$folder" in
    mysql)
      kubectl apply -f "$base/secrets.yml" -n $NAMESPACE
      kubectl apply -f "$base/statefulset.yaml" -n $NAMESPACE
      kubectl apply -f "$base/configmap.yaml" -n $NAMESPACE
      ;;
    redis)
      kubectl apply -f "$base/statefulset_sentinel.yaml" -n $NAMESPACE
      kubectl apply -f "$base/statefulset.yaml" -n $NAMESPACE      
      ;;
    backend)
      kubectl apply -f "$base/secrets.yml" -n $NAMESPACE
      kubectl apply -f "$base/deployment.yaml" -n $NAMESPACE
      kubectl apply -f "$base/hpa.yaml" -n $NAMESPACE
      ;;
    client)
      kubectl apply -f "$base/deployment.yaml" -n $NAMESPACE
      kubectl apply -f "$base/hpa.yaml" -n $NAMESPACE
      ;;
    upload-server|budibase|ingress)
      # Fallback: aplica tudo em ordem qualquer
      for file in "$base"/*.yaml; do
        [ -f "$file" ] && kubectl apply -f "$file" -n $NAMESPACE
      done
      ;;
    grafana|jaeger|prometheus|otel-collector|configmap|pvc_observability)
      for file in "$base"/*.yaml; do
        [ -f "$file" ] && kubectl apply -f "$file" -n $NAMESPACE
      done
      ;;
    *)
      echo "Unknown component folder: $folder"
      ;;
  esac

  if [ -n "$image" ] && [ -n "$container_name" ]; then
    echo "🖼️ Setting image for container '$container_name' in deployment '$deployment_name' to: $image"
    kubectl set image deployment/$deployment_name $container_name=$image -n $NAMESPACE
  fi
}

# Build
if $BUILD_IMAGES; then
  cd E_commerce/
  echo "Building Docker Images..."
  $DEPLOY_FRONTEND && docker build -t $REGISTRY/$FRONTEND_IMAGE:$COMMIT_HASH -f ./client/.docker/Dockerfile.prod ./client
  $DEPLOY_BACKEND && docker build -t $REGISTRY/$BACKEND_IMAGE:$COMMIT_HASH -f ./API/.docker/Dockerfile.prod .
  $DEPLOY_BUDIBASE && docker build -t $REGISTRY/$BUDIBASE_IMAGE:$COMMIT_HASH -f ./budibase/.docker/Dockerfile.prod ./budibase
  $DEPLOY_UPLOAD && docker build -t $REGISTRY/$UPLOAD_IMAGE:$COMMIT_HASH -f ./upload-server/Dockerfile.prod ./upload-server
  cd ..
fi

# Push
if $PUSH_IMAGES; then
  echo "Pushing Docker Images..."
  $DEPLOY_FRONTEND && docker push $REGISTRY/$FRONTEND_IMAGE:$COMMIT_HASH
  $DEPLOY_BACKEND && docker push $REGISTRY/$BACKEND_IMAGE:$COMMIT_HASH
  $DEPLOY_BUDIBASE && docker push $REGISTRY/$BUDIBASE_IMAGE:$COMMIT_HASH
  $DEPLOY_UPLOAD && docker push $REGISTRY/$UPLOAD_IMAGE:$COMMIT_HASH
fi

$DEPLOY_GRAFANA     && apply_component "grafana"            "grafana"             "" ""
$DEPLOY_JAEGER      && apply_component "jaeger"             "jaeger"              "" ""
$DEPLOY_PROMETHEUS  && apply_component "prometheus"         "prometheus"          "" ""
$DEPLOY_OTEL        && apply_component "otel-collector"     "otel-collector"      "" ""
$DEPLOY_CONFIGMAP   && apply_component "configmap"          "configmap"           "" ""
$DEPLOY_PVC         && apply_component "pvc_observability"  "pvc_observability"   "" ""


# Delete individual components
$DELETE_FRONTEND && delete_component "client"
$DELETE_BACKEND && delete_component "backend"
$DELETE_UPLOAD && delete_component "upload-server"
$DELETE_MYSQL && delete_component "mysql"
$DELETE_REDIS && delete_component "redis"
$DELETE_BUDIBASE && delete_component "budibase"
$DELETE_INGRESS && delete_component "ingress"
$DELETE_GRAFANA && delete_component "grafana"
$DELETE_JAEGER && delete_component "jaeger"
$DELETE_PROMETHEUS && delete_component "prometheus"
$DELETE_OTEL && delete_component "otel-collector"
$DELETE_CONFIGMAP && delete_component "configmap"
$DELETE_PVC && delete_component "pvc_observability"

# Delete all
if $DELETE_ALL_DEPLOYMENTS; then
  echo "Deleting ALL components in $NAMESPACE..."
  for dir in client backend cdn upload-server mysql redis budibase ingress; do
    delete_component "$dir"
  done
fi

#                                     folder          deployment                  image                                     container
$DEPLOY_FRONTEND  && apply_component "client"        "client"                    "$REGISTRY/$FRONTEND_IMAGE:$COMMIT_HASH" "client"
$DEPLOY_BACKEND   && apply_component "backend"       "backend"                   "$REGISTRY/$BACKEND_IMAGE:$COMMIT_HASH"  "backend"
$DEPLOY_UPLOAD    && apply_component "upload-server" "upload-server-deployment"  "$REGISTRY/$UPLOAD_IMAGE:$COMMIT_HASH"   "upload-server"
$DEPLOY_BUDIBASE  && apply_component "budibase"      "budibase-deployment"       "$REGISTRY/$BUDIBASE_IMAGE:$COMMIT_HASH" "budibase"
$DEPLOY_INGRESS   && apply_component "ingress"       "ingress"                   ""                                       ""

echo "DONE."