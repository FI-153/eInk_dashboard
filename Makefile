.PHONY: help run test lint format quality docker-build docker-up docker-down setup

.DEFAULT_GOAL := help

help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@echo "  run            Flask debug server on 0.0.0.0:6123 (config from .env)"
	@echo "  test           Run full test suite"
	@echo "  quality        Linting + formatting + auto-fix"
	@echo "  lint           Check linting + formatting"
	@echo "  format         Auto-fix lint issues and format"
	@echo "  setup          Install all dependencies (including dev) into .venv via uv"
	@echo "  docker-build   Build Docker image"
	@echo "  docker-up      Build and run with Docker Compose"
	@echo "  docker-down    Stop Docker containers"

run:
	USE_DOTENV=1 uv run python app.py

test:
	uv run pytest tests/ -v

quality:
	make lint
	make format

lint:
	uv run ruff check .
	uv run ruff format --check .

format:
	uv run ruff check --fix .
	uv run ruff format .

docker-build:
	sudo docker compose build

docker-up:
	sudo docker compose up -d

docker-down:
	sudo docker compose down

setup:
	uv sync
