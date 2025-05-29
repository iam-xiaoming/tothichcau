#!/bin/bash
set -e  # Dừng script nếu có lỗi

IMAGE_NAME="game-art"
IMAGE_TAG="v1.0"
ENV_FILE=".env"
APP_CONTAINER_NAME="game-art"

echo "===> Loading environment variables from $ENV_FILE..."
export $(grep -v '^#' "$ENV_FILE" | xargs)

echo "===> Building Docker image $IMAGE_NAME:$IMAGE_TAG..."
docker build -t "$IMAGE_NAME:$IMAGE_TAG" .

echo "===> Stopping old container (if exists)..."
docker stop "$APP_CONTAINER_NAME" 2>/dev/null || true
docker rm "$APP_CONTAINER_NAME" 2>/dev/null || true

echo "===> Starting new container..."
docker run -d \
    --env-file "$ENV_FILE" \
    --name "$APP_CONTAINER_NAME" \
    -p 8000:8000 \
    "$IMAGE_NAME:$IMAGE_TAG"

echo "===> Deploy complete. All services are running."