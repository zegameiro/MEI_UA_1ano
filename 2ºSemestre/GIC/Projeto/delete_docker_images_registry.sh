#!/bin/bash

registry="registry.deti"
name="g11-bytebazaar/ecom-budibase"
tag="1.1" 

digest=$(curl -sSL -I \
  -H "Accept: application/vnd.docker.distribution.manifest.v2+json" \
  "http://${registry}/v2/${name}/manifests/${tag}" \
  | awk '$1 == "Docker-Content-Digest:" { print $2 }' \
  | tr -d $'\r')

if [ -z "$digest" ]; then
  echo "Error: Could not retrieve digest for ${name}:${tag}"
  exit 1
fi

echo "Deleting ${name}:${tag} (digest: $digest)"
curl -sSL -X DELETE "http://${registry}/v2/${name}/manifests/${digest}" \
  && echo "Successfully deleted ${name}:${tag}" \
  || echo "Failed to delete ${name}:${tag}"
