#!/bin/bash

# Step 1: Pull latest changes from Git
echo "Pulling latest updates from Git..."
git pull

# Step 2: Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Step 3: Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Step 4: Run database migrations
echo "Running Alembic migrations..."
alembic upgrade head

# Step 5: Restart the FastAPI backend service
SERVICE_NAME="pimoo-backend"
echo "Restarting $SERVICE_NAME service..."
sudo systemctl restart $SERVICE_NAME

# Step 6: Check if the service is running
echo "Checking if $SERVICE_NAME is running..."
if systemctl is-active --quiet $SERVICE_NAME; then
    echo "$SERVICE_NAME is running successfully."
else
    echo "Failed to start $SERVICE_NAME. Please check the logs."
fi