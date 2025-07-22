# Makefile for CV & Cover Letter Builder

.PHONY: help install dev-install test lint format clean migrate superuser runserver docker-build docker-up docker-down

# Default target
help:
	@echo "Available commands:"
	@echo "  install      - Install production dependencies"
	@echo "  dev-install  - Install development dependencies"
	@echo "  test         - Run all tests"
	@echo "  lint         - Run linting checks"
	@echo "  format       - Format code with black"
	@echo "  clean        - Clean up temporary files"
	@echo "  migrate      - Run database migrations"
	@echo "  superuser    - Create superuser account"
	@echo "  runserver    - Start development server"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-up    - Start Docker containers"
	@echo "  docker-down  - Stop Docker containers"

# Installation
install:
	pip install -r requirements.txt

dev-install:
	pip install -r requirements.txt
	pip install black flake8 pytest pytest-django coverage

# Testing
test:
	python manage.py test
	@echo "All tests completed!"

test-coverage:
	coverage run --source='.' manage.py test
	coverage report
	coverage html

# Code quality
lint:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=88 --statistics

format:
	black . --line-length=88

# Database
migrate:
	python manage.py migrate

makemigrations:
	python manage.py makemigrations

superuser:
	python manage.py createsuperuser

# Development
runserver:
	python manage.py runserver

shell:
	python manage.py shell

collectstatic:
	python manage.py collectstatic --noinput

# Docker
docker-build:
	docker build -t cv-cover-letter-builder .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

# Cleanup
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/

# Environment setup
setup:
	cp .env.example .env
	@echo "Please edit .env file with your actual configuration"
	python manage.py migrate
	@echo "Setup complete! Run 'make superuser' to create admin account"

# Production
prod-check:
	python manage.py check --deploy
	@echo "Production readiness check complete"

# All-in-one development setup
dev-setup: install migrate
	@echo "Development environment ready!"
	@echo "Run 'make superuser' to create admin account"
	@echo "Run 'make runserver' to start development server"
