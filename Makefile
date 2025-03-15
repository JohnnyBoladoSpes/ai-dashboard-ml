.PHONY: up down dev logs test format clean

up:
	@echo "🚀 Starting all services..."
	docker compose down && docker compose up --build -d

down:
	@echo "🛑 Stopping all services..."
	docker compose down

dev:
	@echo "🚀 Starting FastAPI in development mode..."
	docker compose up -d mongo redis
	uvicorn fastapi_app.main:app --host 0.0.0.0 --port 9000 --reload

logs:
	@echo "📜 Showing FastAPI logs..."
	docker logs -f fastapi_app

format:
	@echo "🖋️  Formatting code with Black..."
	black .

clean:
	@echo "🧹 Cleaning up Docker and cache files..."
	docker system prune -af
	find . -name "__pycache__" -exec rm -rf {} +

status:
	@echo "Checking status of FastAPI service..."
	@if nc -zv 127.0.0.1 9000 > /dev/null 2>&1; then \
		echo "✅ FastAPI service is running"; \
	else \
		echo "❌ FastAPI service is not running"; \
	fi
	@echo "Checking status of MongoDB..."
	@if nc -zv 127.0.0.1 27017 > /dev/null 2>&1; then \
		echo "✅ MongoDB is running"; \
	else \
		echo "❌ MongoDB is not running"; \
	fi
	@echo "Checking status of Redis..."
	@if nc -zv 127.0.0.1 6379 > /dev/null 2>&1; then \
		echo "✅ Redis is running"; \
	else \
		echo "❌ Redis is not running"; \
	fi
