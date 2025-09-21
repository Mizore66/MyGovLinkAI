#!/bin/bash

# EC2 Deployment Script for MCP Server
# This script sets up the environment and installs dependencies

echo "Starting MCP Server deployment on EC2..."

# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Python 3.12 and pip
sudo apt install -y python3.12 python3.12-venv python3-pip git

# Create application directory
APP_DIR="/opt/mcp-server"
sudo mkdir -p $APP_DIR
sudo chown $USER:$USER $APP_DIR

# Navigate to application directory
cd $APP_DIR

# Clone or copy your project files here
# For now, we'll assume files are already copied
echo "Make sure to copy your project files to $APP_DIR"

# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create log directory
sudo mkdir -p /var/log/mcp-server
sudo chown $USER:$USER /var/log/mcp-server

echo "Setup complete!"
echo "Next steps:"
echo "1. Copy your project files to $APP_DIR"
echo "2. Test the server: cd $APP_DIR && source venv/bin/activate && python mcp_server.py"
echo "3. Set up systemd service (see deployment guide)"