.PHONY: up down run test lint format

up:
	docker compose up -d

down:
	docker compose down

run:
	uv run --env-file .env kybr-pipeline

test:
	pytest --lf -vv

lint:
	ruff check

format:
	ruff check --fix