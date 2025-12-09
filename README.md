# GameTable

This application is developed for the courses "Full Stack Development", "Databases for Developers", and "Testing" on the first semester of the PBa Software Development Top-up

## Stack

- DevOps: Docker (compose), GitHub (actions), Azure VPS,
- Backend: UV, Python, FastAPI, MySQL
- Frontend: React, Chakra (perhaps), TypeScript, Bun
- Database Migration: NoSQLMigrator

### Pre-Requirements

- Docker Engine
- Docker Compose
- Bun
- Patience

## Quick Start (3 Steps)

### Step 1: Configure Environment Variables

Create a `.env` file in the `/backend` folder using `.env.example` as a template:

```bash
cp backend/.env.example backend/.env
```

Don't change any values unless you intend to manually create a different user for the database.

### Step 2: Start the Containers

From the root folder, build and run all 5 containers:

```bat
docker compose -f docker-compose.dev.yml up -d
```

You should now have these containers running:

| Container       |     Port      |
| :-------------- | :-----------: |
| Backend Server  |     8000      |
| Frontend Server |     3000      |
| MySQL 8.4       |     3306      |
| mongo 7         |     27017     |
| neo4j           | 7474 and 7687 |

### Step 3: Create schema + tables + triggers + functions + procedures

IF YOU HAVE NOT CREATED A DATABASE WITH TEST DATA YET:

run the file "/db/run_me_first.ddl" in your preferred database program
run the "/db/run_me_second.sql" file in your preferred database program

The first one (the ddl file) creates that Database / schema, the tables, a trigger, etc.

The second one (the sql file) populates the database with real testing data

### OLD Usage guidelines

To run the backend application and a MySQL docker container, \
run the following command from repository root folder

```bash
docker compose -f docker-compose.dev.yml up -d
```

The backend will now be run at localhost:8000 and you endpoints \
can be seen at: \
localhost:8000/docs

The MySQL Database runs at port 3306

If you want to run the frontend as well, then switch to the \
fronted folder and install the node modules with bun:

```bash
cd frontend
bun i
```

Lastly, run your development server with:

```bash
bun run dev
```

The frontend should now be running at port 3000

### Errors You Might Encounter

1. "Command not found" when using docker compose

You're using Docker Compose V1. Use `docker-compose` instead:

```bash
docker-compose -f docker-compose.dev.yml up -d
```

### 2. Internal Server Error

Likely cause: Database hasn't been initialized yet. Run Step 3 above to populate your database.

### 3. Python library errors

Ensure all Python dependencies are installed:

```bash
cd backend
uv sync
```

### 4. Database connection errors

Verify that:

- The MySQL container is running: `docker ps`
- The `.env` file in `/backend` has correct database credentials
- Port 3306 is not blocked by another service

## Need Help?

Contact Wenmin Ye for technical support
