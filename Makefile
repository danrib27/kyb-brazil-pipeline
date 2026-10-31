.PHONY: up down test

up:
	docker compose up -d

down:
	docker compose down

test:
	pytest --lf -vv