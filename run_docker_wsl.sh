#!/bin/bash
# Quick start script for running GCM on WSL with Docker

set -e

echo "======================================"
echo "GCM - Docker Quick Start (WSL)"
echo "======================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found!"
    echo ""
    echo "Please install Docker Desktop for Windows with WSL2 integration:"
    echo "  https://www.docker.com/products/docker-desktop/"
    echo ""
    echo "Or install Docker in WSL:"
    echo "  curl -fsSL https://get.docker.com -o get-docker.sh"
    echo "  sudo sh get-docker.sh"
    echo "  sudo usermod -aG docker \$USER"
    echo ""
    exit 1
fi

echo "✓ Docker is installed"

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Docker daemon is not running!"
    echo ""
    echo "Please start Docker Desktop (Windows) or run:"
    echo "  sudo service docker start"
    echo ""
    exit 1
fi

echo "✓ Docker is running"
echo ""

# Create output directory
mkdir -p output
echo "✓ Created output directory"
echo ""

# Show menu
echo "What would you like to do?"
echo ""
echo "1) Run demo scenarios (generate plots)"
echo "2) Start web application (interactive)"
echo "3) Open Python shell (development)"
echo "4) Build Docker image only"
echo "5) View documentation"
echo ""
read -p "Enter choice (1-5): " choice

case $choice in
    1)
        echo ""
        echo "======================================"
        echo "Running Demo Scenarios..."
        echo "======================================"
        echo ""
        echo "This will:"
        echo "  - Build Docker image (first time only)"
        echo "  - Run 6 different scenarios"
        echo "  - Generate 4 plot files in ./output/"
        echo "  - Take ~1-2 minutes"
        echo ""
        read -p "Press Enter to continue..."

        docker-compose --profile demo up --build

        echo ""
        echo "======================================"
        echo "✓ Demo Complete!"
        echo "======================================"
        echo ""
        echo "View your plots:"
        ls -lh output/*.png
        echo ""
        echo "Open them with:"
        echo "  explorer.exe output\\"
        echo "or"
        echo "  xdg-open output/gcm_scenarios_comprehensive.png"
        echo ""
        ;;

    2)
        echo ""
        echo "======================================"
        echo "Starting Web Application..."
        echo "======================================"
        echo ""
        echo "This will:"
        echo "  - Build Docker image (first time only)"
        echo "  - Start Flask web server"
        echo "  - Open on http://localhost:5000"
        echo ""
        read -p "Press Enter to continue..."

        echo ""
        echo "Starting server... (Press Ctrl+C to stop)"
        echo ""
        echo "Once started, open your browser to:"
        echo "  http://localhost:5000"
        echo ""

        docker-compose --profile web up --build
        ;;

    3)
        echo ""
        echo "======================================"
        echo "Opening Python Shell..."
        echo "======================================"
        echo ""
        echo "This will:"
        echo "  - Build Docker image (first time only)"
        echo "  - Start interactive Python shell"
        echo "  - GCM modules will be importable"
        echo ""
        echo "Try these commands:"
        echo "  from gcm import GCM"
        echo "  model = GCM(nlon=32, nlat=16, nlev=10)"
        echo "  model.initialize(profile='tropical')"
        echo "  model.run(duration_days=1)"
        echo ""
        read -p "Press Enter to continue..."

        docker-compose --profile shell run gcm-shell bash
        ;;

    4)
        echo ""
        echo "======================================"
        echo "Building Docker Image..."
        echo "======================================"
        echo ""

        docker-compose build

        echo ""
        echo "✓ Build complete!"
        echo ""
        echo "Run scenarios with:"
        echo "  docker-compose --profile demo up"
        echo ""
        echo "Start web app with:"
        echo "  docker-compose --profile web up"
        echo ""
        ;;

    5)
        echo ""
        echo "======================================"
        echo "Documentation"
        echo "======================================"
        echo ""
        echo "Available documentation files:"
        echo ""
        echo "1. DOCKER_SETUP.md - Complete Docker guide"
        echo "2. AUTOMATED_DEPLOYMENT.md - GitHub Pages deployment"
        echo "3. README.md - General overview"
        echo "4. docs/ - Web documentation"
        echo ""
        echo "Quick commands:"
        echo ""
        echo "  # Run demo scenarios"
        echo "  docker-compose --profile demo up"
        echo ""
        echo "  # Start web app"
        echo "  docker-compose --profile web up"
        echo ""
        echo "  # Python shell"
        echo "  docker-compose --profile shell run gcm-shell"
        echo ""
        echo "  # Stop all containers"
        echo "  docker-compose down"
        echo ""
        echo "View full documentation:"
        echo "  cat DOCKER_SETUP.md"
        echo "  less DOCKER_SETUP.md"
        echo ""
        ;;

    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "Done! 🎉"
echo ""
