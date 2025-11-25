.PHONY: frontend backend migrator scraper setup

frontend:
	cd frontend && bun install

backend:
	cd backend && uv sync

migrator:
	cd NoSQLMigrator && uv sync

scraper:
	cd data-aggregator && uv sync

setup: frontend backend migrator scraper
