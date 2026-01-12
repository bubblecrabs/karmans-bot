.PHONY: help build up down down-v alembic-init migration upgrade logs pre-commit-clean pre-commit-all

help:
	@echo "Available commands:"
	@echo "  make build            - Build Docker images"
	@echo "  make up               - Build and start containers"
	@echo "  make down             - Stop containers"
	@echo "  make down-v           - Stop containers and remove volumes"
	@echo "  make alembic-init     - Initialize Alembic with async template"
	@echo "  make migration        - Create new Alembic migration"
	@echo "  make upgrade          - Apply migrations"
	@echo "  make logs             - Show logs"
	@echo "  make pre-commit-clean - Clean pre-commit cache"
	@echo "  make pre-commit-all   - Run pre-commit on all files"

build:
	docker compose build

up:
	docker compose up -d --build

down:
	docker compose down

down-v:
	docker compose down -v

alembic-init:
	docker compose exec bot alembic init -t async migrations

migration:
	docker compose exec bot alembic revision --autogenerate -m "$(msg)"

upgrade:
	docker compose exec bot alembic upgrade head

downgrade:
	docker compose exec bot alembic downgrade -1

alembic-init-local:
	uv run alembic init -t async alembic

migration-local:
	uv run alembic revision --autogenerate -m "$(msg)"

upgrade-local:
	uv run alembic upgrade head

downgrade-local:
	uv run alembic downgrade -1

logs:
	docker compose logs -f bot

pre-commit-clean:
	uv run pre-commit clean

pre-commit-all:
	uv run pre-commit run --all-files
