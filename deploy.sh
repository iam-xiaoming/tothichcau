#!/bin/bash
set -e  # Dừng script nếu có lỗi

NETWORK_NAME="game-net"
IMAGE_NAME="game-art"
IMAGE_TAG="v1.0"
ENV_FILE=".env"
APP_CONTAINER_NAME="game-art"
CELERY_WORKER_NAME="celery_worker"
CELERY_BEAT_NAME="celery_beat"
REDIS_CONTAINER_NAME="redis"

echo "===> Checking Docker network..."
if ! docker network ls | grep -qw "$NETWORK_NAME"; then
    echo "Creating network '$NETWORK_NAME'..."
    docker network create "$NETWORK_NAME"
else
    echo "Network '$NETWORK_NAME' already exists."
fi

echo "===> Building Docker image ${IMAGE_NAME}:${IMAGE_TAG}..."
docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .

echo "===> Removing old containers if exist..."
docker rm -f $APP_CONTAINER_NAME $CELERY_WORKER_NAME $CELERY_BEAT_NAME $REDIS_CONTAINER_NAME 2>/dev/null || true

echo "===> Starting Redis container..."
docker run -d --name $REDIS_CONTAINER_NAME --network "$NETWORK_NAME" redis:7-alpine

echo "===> Starting Django app container ($APP_CONTAINER_NAME)..."
docker run -d \
  --name $APP_CONTAINER_NAME \
  --network "$NETWORK_NAME" \
  -p 8000:8000 \
  -v "$(pwd)":/app \
  --env-file "$ENV_FILE" \
  ${IMAGE_NAME}:${IMAGE_TAG}

echo "===> Running Django migrations inside app container..."
docker exec $APP_CONTAINER_NAME python manage.py makemigrations
docker exec $APP_CONTAINER_NAME python manage.py migrate

echo "===> Collecting static files..."
docker exec $APP_CONTAINER_NAME python manage.py collectstatic --noinput

echo "===> Starting Celery worker container ($CELERY_WORKER_NAME)..."
docker run -d \
  --name $CELERY_WORKER_NAME \
  --network "$NETWORK_NAME" \
  -v "$(pwd)":/app \
  --env-file "$ENV_FILE" \
  ${IMAGE_NAME}:${IMAGE_TAG} \
  celery -A GameArt worker --loglevel=info

echo "===> Starting Celery beat container ($CELERY_BEAT_NAME)..."
docker run -d \
  --name $CELERY_BEAT_NAME \
  --network "$NETWORK_NAME" \
  -v "$(pwd)":/app \
  --env-file "$ENV_FILE" \
  ${IMAGE_NAME}:${IMAGE_TAG} \
  celery -A GameArt beat -l info

# Build RTMP server
echo "===> Building RTMP server image..."
docker build -f Dockerfile.rtmp -t rtmp-server .

# Ensure directories exist
sudo mkdir -p /opt/data/hls /home/ec2-user/tothichcau/www/static
sudo chmod -R 777 /opt/data/hls /home/ec2-user/tothichcau/www/static
sudo chown -R ec2-user:ec2-user /opt/data/hls /home/ec2-user/tothichcau/www/static

echo "===> Starting RTMP server container..."
docker run -d \
  --name rtmp-server \
  --network "$NETWORK_NAME" \
  -p 1935:1935 \
  -p 8080:80 \
  -v /opt/data/hls:/opt/data/hls \
  -v /home/ec2-user/tothichcau/www/static:/www/static \
  rtmp-server

echo "===> Deploy complete. All services are running."