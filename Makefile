PYTHON ?= python3

.PHONY: help run test lint format docker-build docker-up docker-down setup

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
	@echo "  setup          Create venv and install all dependencies (including dev)"
	@echo "  docker-build   Build Docker image"
	@echo "  docker-up      Build and run with Docker Compose"
	@echo "  docker-down    Stop Docker containers"

run:
	USE_DOTENV=1 $(PYTHON) app.py

test:
	$(PYTHON) -m pytest tests/ -v

quality:
	make lint
	make format

lint:
	ruff check .
	ruff format --check .

format:
	ruff check --fix .
	ruff format .

docker-build:
	sudo docker compose build

docker-up:
	sudo docker compose up -d

docker-down:
	sudo docker compose down

setup:
	$(PYTHON) -m venv .venv
	. .venv/bin/activate && pip install -r requirements-dev.txt