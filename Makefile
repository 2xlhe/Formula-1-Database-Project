# Makefile for FIA Database Manager

# Python version detection
REQUIRED_PYTHON_VERSION := 3.12

.PHONY: help install docker-up setup-db setup-db-force run clean venv

# Default target
help:
	@echo "Available commands:"
	@echo "  make install        - Install Python dependencies in virtual environment"
	@echo "  make docker-up      - Start PostgreSQL container"
	@echo "  make setup-db       - Initialize database tables and data (if not exists)"
	@echo "  make setup-db-force - Force re-run all database migrations"
	@echo "  make run            - Setup everything and run application"
	@echo "  make clean          - Stop and remove containers"
	@echo "  make reset-db       - Reset database completely (removes persistent data)"
	@echo "  make clean-db-volumes - Clean database volumes only"
	@echo "  make clean-docker   - Clean all Docker resources"
	@echo "  make clean-all      - Clean everything including virtual environment"

# Install Python dependencies using uv
install: venv
	@echo "Installing Python dependencies with uv..."
	@uv sync
	@echo "✓ Dependencies installed"

# Start Docker Compose services
docker-up:
	@echo "Starting PostgreSQL container..."
	@if [ "$$(docker ps -q -f name=fia-postgres)" ]; then \
		echo "✓ PostgreSQL container is already running"; \
	else \
		if [ "$$(docker ps -aq -f name=fia-postgres)" ]; then \
			echo "Starting existing PostgreSQL container..."; \
			docker start fia-postgres; \
		else \
			echo "Creating and starting PostgreSQL container..."; \
			docker-compose up -d; \
		fi; \
		echo "Waiting for PostgreSQL to be ready..."; \
		sleep 5; \
	fi
	@echo "✓ PostgreSQL container is running"

# Setup database tables and initial data
setup-db: docker-up
	@echo "Setting up database..."
	@if docker exec fia-postgres psql -U postgres -d fia -t -c "SELECT 1 FROM information_schema.tables WHERE table_name='drivers'" 2>/dev/null | grep -q 1; then \
		echo "✓ Database tables already exist, skipping setup"; \
	else \
		echo "Running database migrations..."; \
		echo "  1/6 Loading database dump (this may take 5-10 seconds)..."; \
		docker exec fia-postgres psql -U postgres -d fia -f /docker-entrypoint-initdb.d/dump.sql; \
		echo "  2/6 Creating tables and initial data..."; \
		docker exec fia-postgres psql -U postgres -d fia -f /docker-entrypoint-initdb.d/create_insert.sql; \
		echo "  3/6 Creating views..."; \
		docker exec fia-postgres psql -U postgres -d fia -f /docker-entrypoint-initdb.d/views.sql; \
		echo "  4/6 Creating functions and dashboards..."; \
		docker exec fia-postgres psql -U postgres -d fia -f /docker-entrypoint-initdb.d/dashboards.sql; \
		echo "  5/6 Creating triggers..."; \
		docker exec fia-postgres psql -U postgres -d fia -f /docker-entrypoint-initdb.d/triggers.sql; \
		echo "  6/6 Creating indexes..."; \
		docker exec fia-postgres psql -U postgres -d fia -f /docker-entrypoint-initdb.d/index.sql; \
		echo "✓ Database setup completed successfully"; \
	fi

# Force setup database (re-run all migrations)
setup-db-force: docker-up
	@echo "Force running all database migrations..."
	@echo "  1/6 Loading database dump (this may take 5-10 seconds)..."
	@docker exec fia-postgres psql -U postgres -d fia -f /docker-entrypoint-initdb.d/dump.sql
	@echo "  2/6 Creating tables and initial data..."
	@docker exec fia-postgres psql -U postgres -d fia -f /docker-entrypoint-initdb.d/create_insert.sql
	@echo "  3/6 Creating views..."
	@docker exec fia-postgres psql -U postgres -d fia -f /docker-entrypoint-initdb.d/views.sql
	@echo "  4/6 Creating functions and dashboards..."
	@docker exec fia-postgres psql -U postgres -d fia -f /docker-entrypoint-initdb.d/dashboards.sql
	@echo "  5/6 Creating triggers..."
	@docker exec fia-postgres psql -U postgres -d fia -f /docker-entrypoint-initdb.d/triggers.sql
	@echo "  6/6 Creating indexes..."
	@docker exec fia-postgres psql -U postgres -d fia -f /docker-entrypoint-initdb.d/index.sql
	@echo "✓ All database migrations completed successfully"

# Main target: setup everything and run application using uv
run: install setup-db
	@echo "Starting FIA Database Manager..."
	@uv run src/main.py

# Clean up Docker containers
clean:
	@echo "Stopping and removing containers..."
	docker-compose down
	docker-compose down --volumes
	@echo "✓ Containers cleaned up"

# Reset database completely (removes persistent volume)
reset-db:
	@echo "🗑️  Resetting database (removing containers and volumes)..."
	docker-compose down -v
	@echo "🐳 Starting fresh PostgreSQL container..."
	docker-compose up -d
	@echo "⏳ Waiting for PostgreSQL to be ready..."
	sleep 10
	@echo "✅ Fresh database is ready!"

# Clean database volumes only (keeps container)
clean-db-volumes:
	@echo "🧹 Cleaning database volumes..."
	docker-compose down -v
	@echo "✅ Database volumes cleaned"

# Complete cleanup including orphaned containers
clean-docker:
	@echo "🧹 Cleaning up all Docker resources for this project..."
	docker-compose down -v --remove-orphans
	docker volume prune -f

# Clean everything including virtual environment
clean-all: clean
	@echo "Removing virtual environment..."
	rm -rf venv
	@echo "✓ Everything cleaned up"
