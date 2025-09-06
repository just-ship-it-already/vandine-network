#!/bin/bash
# Install Docker on Ubuntu/WSL2

echo "Installing Docker on WSL2..."

# Update package index
echo "Updating package index..."
sudo apt-get update

# Install prerequisites
echo "Installing prerequisites..."
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Add Docker's official GPG key
echo "Adding Docker GPG key..."
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Set up the stable repository
echo "Adding Docker repository..."
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
echo "Installing Docker Engine..."
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Install Docker Compose standalone
echo "Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add current user to docker group
echo "Adding user to docker group..."
sudo usermod -aG docker $USER

# Start Docker service
echo "Starting Docker service..."
sudo service docker start

# Verify installation
echo "Verifying installation..."
docker --version
docker-compose --version

echo ""
echo "Docker installation complete!"
echo "IMPORTANT: You need to log out and log back in for group changes to take effect."
echo "Or run: newgrp docker"
echo ""
echo "After that, you can continue with the deployment."