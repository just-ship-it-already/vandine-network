.PHONY: help build up down logs shell migrate test clean populate status restart backup

# Default target
help:
	@echo "Available commands:"
	@echo "  make build      - Build Docker images"
	@echo "  make up         - Start all services"
	@echo "  make down       - Stop all services"
	@echo "  make restart    - Restart all services"
	@echo "  make logs       - View logs (all services)"
	@echo "  make shell      - Django shell"
	@echo "  make migrate    - Run Django migrations"
	@echo "  make test       - Run all tests"
	@echo "  make populate   - Populate sample data"
	@echo "  make status     - Show service status"
	@echo "  make clean      - Clean up containers and volumes"
	@echo "  make backup     - Backup database"
	@echo ""
	@echo "Service-specific logs:"
	@echo "  make logs-django  - Django logs"
	@echo "  make logs-fastapi - FastAPI logs"
	@echo "  make logs-celery  - Celery logs"
	@echo "  make logs-nginx   - Nginx logs"

# Build all Docker images
build:
	docker-compose build

# Start all services
up:
	docker-compose up -d
	@echo "Waiting for services to be ready..."
	@sleep 5
	@make status

# Stop all services
down:
	docker-compose down

# Restart all services
restart:
	@make down
	@make up

# View logs for all services
logs:
	docker-compose logs -f

# Service-specific logs
logs-django:
	docker-compose logs -f django

logs-fastapi:
	docker-compose logs -f fastapi

logs-celery:
	docker-compose logs -f celery celery-beat

logs-nginx:
	docker-compose logs -f nginx

# Django shell
shell:
	docker-compose exec django python manage.py shell

# Django shell_plus (with models auto-imported)
shell-plus:
	docker-compose exec django python manage.py shell_plus

# Run Django migrations
migrate:
	docker-compose exec django python manage.py makemigrations
	docker-compose exec django python manage.py migrate

# Create Django superuser
superuser:
	docker-compose exec django python manage.py createsuperuser

# Collect static files
collectstatic:
	docker-compose exec django python manage.py collectstatic --noinput

# Run all tests
test:
	@echo "Running Django tests..."
	docker-compose exec django pytest -v
	@echo "Running FastAPI tests..."
	docker-compose exec fastapi pytest -v

# Run Django tests only
test-django:
	docker-compose exec django pytest -v

# Run FastAPI tests only
test-fastapi:
	docker-compose exec fastapi pytest -v

# Populate sample data
populate:
	docker-compose exec django python scripts/populate_data.py

# Show service status
status:
	@echo "Service Status:"
	@docker-compose ps
	@echo ""
	@echo "Health Checks:"
	@curl -s http://localhost/health || echo "Nginx: Not responding"
	@curl -s http://localhost:8000/health/ || echo "Django: Not responding"
	@curl -s http://localhost:8001/health || echo "FastAPI: Not responding"

# Clean up containers and volumes (WARNING: This will delete all data!)
clean:
	@echo "WARNING: This will delete all containers and volumes!"
	@read -p "Are you sure? [y/N] " confirm; \
	if [ "$$confirm" = "y" ]; then \
		docker-compose down -v; \
		echo "Cleanup complete"; \
	else \
		echo "Cleanup cancelled"; \
	fi

# Backup database
backup:
	@mkdir -p backups
	@BACKUP_FILE="backups/vandine_db_$$(date +%Y%m%d_%H%M%S).sql"; \
	docker-compose exec -T postgres pg_dump -U ${POSTGRES_USER} ${POSTGRES_DB} > $$BACKUP_FILE; \
	echo "Database backed up to: $$BACKUP_FILE"

# Restore database from backup
restore:
	@if [ -z "$(FILE)" ]; then \
		echo "Usage: make restore FILE=backups/vandine_db_YYYYMMDD_HHMMSS.sql"; \
		exit 1; \
	fi
	@echo "Restoring from: $(FILE)"
	@docker-compose exec -T postgres psql -U ${POSTGRES_USER} ${POSTGRES_DB} < $(FILE)
	@echo "Database restored"

# Development setup
dev-setup:
	@cp .env.example .env
	@echo "Created .env file from .env.example"
	@echo "Please edit .env file with your configuration"
	@make build
	@make up
	@make migrate
	@make superuser

# Production deployment
deploy:
	@echo "Deploying to production..."
	@docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
	@make migrate
	@make collectstatic

# Check code style
lint:
	@echo "Checking Django code..."
	docker-compose exec django black --check .
	docker-compose exec django flake8 .
	@echo "Checking FastAPI code..."
	docker-compose exec fastapi black --check .
	docker-compose exec fastapi mypy .

# Format code
format:
	@echo "Formatting Django code..."
	docker-compose exec django black .
	@echo "Formatting FastAPI code..."
	docker-compose exec fastapi black .

# Monitor logs in real-time with filtering
monitor:
	@docker-compose logs -f | grep -E "(ERROR|WARNING|CRITICAL)"

# Quick health check
health:
	@curl -s http://localhost/health && echo " - Nginx: OK" || echo " - Nginx: FAIL"
	@curl -s http://localhost:8000/health/ && echo " - Django: OK" || echo " - Django: FAIL"
	@curl -s http://localhost:8001/health && echo " - FastAPI: OK" || echo " - FastAPI: FAIL"
	@docker-compose exec -T postgres pg_isready && echo " - PostgreSQL: OK" || echo " - PostgreSQL: FAIL"
	@docker-compose exec -T redis redis-cli ping && echo " - Redis: OK" || echo " - Redis: FAIL"