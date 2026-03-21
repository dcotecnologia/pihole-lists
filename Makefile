BRANCH := $(shell git rev-parse --abbrev-ref HEAD)
DOCKER_COMPOSE_CMD := docker-compose
UV_CMD := uv
PYTHON_CMD := python

.DEFAULT_GOAL := help

.PHONY: help cleanup lint build sync lock compile readme

help: ## Show available commands
	@awk 'BEGIN {FS = ":.*##"; printf "Usage: make <target>\n\nTargets:\n"} /^[a-zA-Z_-]+:.*##/ {printf "  %-12s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

cleanup: ## Run list cleanup routine in Docker
	$(DOCKER_COMPOSE_CMD) run --rm --remove-orphans cleanup

lint: ## Run pre-commit checks
	pre-commit run --all-files

build: ## Build Docker image
	$(DOCKER_COMPOSE_CMD) build

sync: ## Sync dependencies from uv.lock
	$(UV_CMD) sync --frozen --no-install-project

lock: ## Regenerate uv.lock from pyproject.toml
	$(UV_CMD) lock

compile: ## Generate combined output files (optional: LISTS=ads,porn)
	LISTS="$(LISTS)" $(UV_CMD) run $(PYTHON_CMD) src/build.py

readme: ## Print markdown rows for README list table
	$(UV_CMD) run $(PYTHON_CMD) src/readme_list.py

import:
	$(UV_CMD) run $(PYTHON_CMD) src/import.py

test:
	$(UV_CMD) run PYTHONPATH=. pytest tests/