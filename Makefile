### Commands abbreviation
DEV_COMPOSE=docker compose -f docker-compose.dev.yml

### Env / Dev VARS
FRONTEND-SERVICE=frontend-server
BACKEND-SERVICE=backend-server


.PHONY: frontend backend migrator scraper setup

gp:
	git pull

### Install Dependencies!
frontend:
	cd frontend && bun install

backend:
	cd backend && uv sync

migrator:
	cd NoSQLMigrator && uv sync

scraper:
	cd data-aggregator && uv sync

setup: frontend backend migrator scraper


### Build and Run Docker Containers and Images
down:
	$(DEV_COMPOSE) down
	cd NoSQLMigrator/ && docker compose down

up:
	$(DEV_COMPOSE) up -d

build-frontend:
	$(DEV_COMPOSE) build $(FRONTEND-SERVICE) --no-cache

build-backend:
	$(DEV_COMPOSE) build $(BACKEND-SERVICE) --no-cache

build-migrator:
	cd NoSQLMigrator/ && docker compose build --no-cache

build: build-frontend build-backend build-migrator
	@echo "YAY. Since you are seeing this message, your build has definitely potentially succeeded."

up-backend:
	@echo "Starting Backend container"
	$(DEV_COMPOSE) up -d $(BACKEND-SERVICE)

### Install EVERYTHING LETSA GOOOO
install: gp, frontend, backend, migrator, scraper, build-frontend, build-backend, build-migrator
	@echo "Wow! You did it. You successfully (maybe) installed all the dependencies and successfully (maybe) build all the images."
	@echo "Now try using 'make up' to start all the containers!"
