#!/bin/bash

# Deploy script cho Backend

set -e

echo "🚀 Starting Backend Deployment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if docker-compose is available
if command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE="docker-compose"
elif docker compose version &> /dev/null; then
    DOCKER_COMPOSE="docker compose"
else
    echo "❌ docker-compose is not available. Please install docker-compose."
    exit 1
fi

echo "✅ Docker and docker-compose are available"

# Build and start services
echo "🏗️  Building and starting services..."
$DOCKER_COMPOSE up --build -d

# Wait for health check
echo "⏳ Waiting for backend to be healthy..."
max_attempts=30
attempt=1

while [ $attempt -le $max_attempts ]; do
    if curl -f http://localhost:8000/docs &> /dev/null; then
        echo "✅ Backend is healthy!"
        break
    fi

    echo "Attempt $attempt/$max_attempts: Backend not ready yet..."
    sleep 5
    ((attempt++))
done

if [ $attempt -gt $max_attempts ]; then
    echo "❌ Backend failed to start properly"
    $DOCKER_COMPOSE logs backend
    exit 1
fi

echo ""
echo "🎉 Backend deployed successfully!"
echo ""
echo "📋 Useful commands:"
echo "  View logs: $DOCKER_COMPOSE logs -f backend"
echo "  Stop: $DOCKER_COMPOSE down"
echo "  Restart: $DOCKER_COMPOSE restart backend"
echo ""
echo "📖 API Documentation: http://localhost:8000/docs"
echo "🔄 Realtime logs: http://localhost:8000/docs (with logs enabled)"