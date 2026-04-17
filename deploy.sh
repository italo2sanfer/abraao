#!/bin/bash

echo '###> 1. Load variables from .env ...'
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
else
    echo "Error: .env file not found!"
    exit 1
fi
FULL_PATH="ghcr.io/$GITHUB_USER/$GITHUB_IMAGE_NAME"

echo "###> 2. Logging into GHCR..."
docker login ghcr.io -u $GITHUB_USER

echo "###> 3. Building $FULL_PATH:$APP_VERSION..."
docker build -f Dockerfile.prod \
  --build-arg APP_DESCRIPTION="$APP_DESCRIPTION" \
  --build-arg APP_PORT="$APP_PORT" \
  --build-arg GITHUB_USER="$GITHUB_USER" \
  --build-arg GITHUB_REPO="$GITHUB_REPO" \
  -t $FULL_PATH:$APP_VERSION .

echo "###> 4. Tag and Push ..."
docker tag $FULL_PATH:$APP_VERSION $FULL_PATH:latest

echo "###> 5. Pushing to GitHub..."
docker push $FULL_PATH:$APP_VERSION
docker push $FULL_PATH:latest

echo "###> 6. Successfully deployed version $APP_VERSION on port $APP_PORT!"
