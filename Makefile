PYTHON ?= python3

.PHONY: run test lint format docker-build docker-up docker-down setup

run:
	$(PYTHON) app.py

test:
	$(PYTHON) -m pytest tests/ -v

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
	pip3 install -r requirements-dev.txt
