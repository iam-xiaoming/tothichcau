#!/bin/bash
set -e

NETWORK_NAME="game-net"
IMAGE_NAME="game-art"
IMAGE_TAG="v1.0"

echo "Checking Docker network..."
if ! docker network ls | grep -q "$NETWORK_NAME"; then
    echo "Creating network $NETWORK_NAME..."
    docker network create "$NETWORK_NAME"
else
    echo "Network $NETWORK_NAME already exists."
fi

echo "Building Docker image..."
docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .

echo "Removing old containers..."
docker rm -f game-art celery_worker redis 2>/dev/null || true

echo "Starting Redis container..."
docker run -d --name redis --network "$NETWORK_NAME" redis:7-alpine

echo "Starting game-art container..."
docker run -d \
    --name game-art \
    --network "$NETWORK_NAME" \
    -p 8000:8000 \
    -v $(pwd):/app \
    --env-file .env \
    ${IMAGE_NAME}:${IMAGE_TAG}

echo "Running Django migrations..."
docker exec game-art python manage.py migrate

echo "Collecting static files to S3..."
docker exec game-art python manage.py collectstatic --noinput

echo "Starting Celery worker container..."
docker run -d \
    --name celery_worker \
    --network "$NETWORK_NAME" \
    -v $(pwd):/app \
    --env-file .env \
    ${IMAGE_NAME}:${IMAGE_TAG} \
    celery -A GameArt worker --loglevel=info

echo "Deploy complete. All services are up!"