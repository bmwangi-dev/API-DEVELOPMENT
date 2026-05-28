COMPOSE ?= docker compose
API_SERVICE ?= api

.DEFAULT_GOAL := help

.PHONY: help env init build up down restart ps logs api-logs db-logs rustfs-logs shell db-shell test clean reset

help:
	@echo "Habit Tracker API commands"
	@echo ""
	@echo "  make env         Create .env from .env.example when missing"
	@echo "  make init        Create .env, build images, and start the full stack"
	@echo "  make build       Build the API image"
	@echo "  make up          Start containers in the background"
	@echo "  make down        Stop and remove containers"
	@echo "  make restart     Recreate containers after config/code changes"
	@echo "  make ps          Show container status"
	@echo "  make logs        Follow all service logs"
	@echo "  make api-logs    Follow API logs"
	@echo "  make db-logs     Follow PostgreSQL logs"
	@echo "  make rustfs-logs Follow RustFS logs"
	@echo "  make shell       Open a shell in the API container"
	@echo "  make db-shell    Open psql in the PostgreSQL container"
	@echo "  make test        Run pytest inside the API container"
	@echo "  make clean       Stop containers and remove orphan containers"
	@echo "  make reset       Stop containers and remove volumes"

env:
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "Created .env from .env.example"; \
	else \
		echo ".env already exists"; \
	fi

init: env
	$(COMPOSE) up -d --build

build:
	$(COMPOSE) build

up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

restart:
	$(COMPOSE) up -d --build --force-recreate

ps:
	$(COMPOSE) ps

logs:
	$(COMPOSE) logs -f

api-logs:
	$(COMPOSE) logs -f api

db-logs:
	$(COMPOSE) logs -f db

rustfs-logs:
	$(COMPOSE) logs -f rustfs

shell:
	$(COMPOSE) exec $(API_SERVICE) sh

db-shell:
	$(COMPOSE) exec db psql -U "$${POSTGRES_USER:-habittracker}" -d "$${POSTGRES_DB:-habittracker}"

test:
	$(COMPOSE) exec $(API_SERVICE) python -m pytest

clean:
	$(COMPOSE) down --remove-orphans

reset:
	$(COMPOSE) down --volumes --remove-orphans
