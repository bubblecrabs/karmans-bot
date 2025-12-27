.PHONY: help build up down down-v migration upgrade logs pre-commit pre-commit-all

help:
	@echo "Available commands:"
	@echo "  make build           - Build Docker images"
	@echo "  make up              - Build and start containers"
	@echo "  make down            - Stop containers"
	@echo "  make down-v          - Stop containers and remove volumes"
	@echo "  make migration       - Create new Alembic migration"
	@echo "  make upgrade         - Apply migrations"
	@echo "  make logs            - Show logs"
	@echo "  make pre-commit      - Clean pre-commit cache"
	@echo "  make pre-commit-all  - Run pre-commit on all files"

build:
	docker compose build

up:
	docker compose up -d --build

down:
	docker compose down

down-v:
	docker compose down -v

migration:
	docker compose exec bot alembic revision --autogenerate -m "$(msg)"

upgrade:
	docker compose exec bot alembic upgrade head

logs:
	docker compose logs -f bot

pre-commit:
	uv run pre-commit clean

pre-commit-all:
	uv run pre-commit run --all-files
