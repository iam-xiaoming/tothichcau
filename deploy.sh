#!/bin/bash

# Tên mạng dùng chung cho các container
NETWORK_NAME="game-net"

echo "Checking Docker network..."
if ! docker network ls | grep -q "$NETWORK_NAME"; then
    echo "Creating network $NETWORK_NAME..."
    docker network create "$NETWORK_NAME"
else
    echo "Network $NETWORK_NAME already exists."
fi

echo "Building Docker image..."
docker build -t game-art:v1.0 .

echo "Stopping old containers..."
docker stop game-art celery_worker redis 2>/dev/null

echo "Removing old containers..."
docker rm game-art celery_worker redis 2>/dev/null

echo "Starting Redis container..."
docker run -d --name redis --network "$NETWORK_NAME" redis:7-alpine

echo "Starting game-art container..."
docker run -d \
    --name game-art \
    --network "$NETWORK_NAME" \
    -p 8000:8000 \
    -v $(pwd):/app \
    --env-file .env \
    game-art:v1.0

echo "Starting Celery worker container..."
docker run -d \
    --name celery_worker \
    --network "$NETWORK_NAME" \
    -v $(pwd):/app \
    --env-file .env \
    game-art:v1.0 \
    celery -A GameArt worker --loglevel=info

echo "Deploy complete. All services are up!"