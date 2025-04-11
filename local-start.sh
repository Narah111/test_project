#!/bin/bash

# Default to port 5000 if no argument is provided
APP_PORT=${1:-5000}

echo "Starting the application on port $APP_PORT..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "[ERROR] Docker is not installed. Please install Docker and try again."
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "[ERROR] Docker is not running. Please start Docker Desktop or the Docker daemon."
    exit 1
fi

# Check if port 5432 is in use (commonly used by Postgres)
if lsof -i :5432 &> /dev/null; then
    echo "[ERROR] Port 5432 is already in use. Please stop the process using it or change the port in docker-compose.yml."
    exit 1
fi

# Run docker-compose with the specified or default port
APP_PORT=$APP_PORT docker compose up --build

# Check if docker-compose failed
if [ $? -ne 0 ]; then
    echo
    echo "[ERROR] Docker Compose failed to start. Maybe port $APP_PORT was already in use?"
    echo
    echo "Usage: ./local-start.sh [PORT]"
    echo "Example: ./local-start.sh 5001 (to run on port 5001)"
    exit 1
fi