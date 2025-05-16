#!/bin/bash

echo "Building image..."
docker build -t game-art:debug .

echo "Stopping old containers..."
docker stop game-art celery_worker

echo "Removing old containers..."
docker rm game-art celery_worker

echo "Starting new containers..."
docker run -d --name game-art --network game-net -p 8000:8000 -v $(pwd):/app --env-file .env game-art:debug
docker run -d --name celery_worker --network game-net -v $(pwd):/app --env-file .env game-art:debug celery -A GameArt worker --loglevel=info

echo "Deploy complete."

