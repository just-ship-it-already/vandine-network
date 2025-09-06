#!/bin/bash
# Deployment script for Vandine Network Monitor

set -e  # Exit on error

echo "🚀 Vandine Network Monitor Deployment Script"
echo "==========================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 1. Check Docker installation
echo "📋 Checking prerequisites..."
if ! command_exists docker; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "Run the Docker installation commands provided earlier."
    exit 1
fi

if ! command_exists docker-compose; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker version: $(docker --version)"
echo "✅ Docker Compose version: $(docker-compose --version)"

# 2. Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration"
    exit 1
else
    echo "✅ .env file found"
fi

# 3. Build Docker images
echo ""
echo "🔨 Building Docker images..."
docker-compose build

# 4. Start services
echo ""
echo "🚀 Starting services..."
docker-compose up -d

# 5. Wait for services to be ready
echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

# 6. Check service health
echo ""
echo "🏥 Checking service health..."
docker-compose ps

# 7. Run migrations
echo ""
echo "🗄️ Running database migrations..."
docker-compose exec -T django python manage.py migrate

# 8. Collect static files
echo ""
echo "📦 Collecting static files..."
docker-compose exec -T django python manage.py collectstatic --noinput

# 9. Create superuser (if not exists)
echo ""
echo "👤 Creating superuser..."
docker-compose exec -T django python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@vandine.us', 'adm1npassw0rD')
    print('Superuser created successfully!')
else:
    print('Superuser already exists.')
"

# 10. Populate sample data (optional)
read -p "Do you want to populate sample data? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📊 Populating sample data..."
    docker-compose exec -T django python scripts/populate_data.py
fi

# 11. Show access information
echo ""
echo "✅ Deployment complete!"
echo ""
echo "🌐 Access your application at:"
echo "   - Dashboard: http://localhost"
echo "   - Admin Panel: http://localhost/admin"
echo "   - FastAPI Docs: http://localhost/api/v1/docs"
echo ""
echo "📝 Login credentials:"
echo "   - Username: admin"
echo "   - Password: adm1npassw0rD"
echo ""
echo "📊 View logs with: docker-compose logs -f"
echo "🛑 Stop services with: docker-compose down"
echo ""

# 12. Optional: Setup Cloudflare tunnel
echo "☁️  Cloudflare Tunnel:"
echo "   Your tunnel ID is configured: 153cc7a6-9ab5-4172-b4cc-eb21e5b524cd"
echo "   To connect the tunnel, run cloudflared on your host machine."
echo ""