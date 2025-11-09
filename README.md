# GameTable

This application is developed for the courses "Full Stack Development", "Databases for Developers", and "Testing" on the first semester of the PBa Software Development Top-up

## Stack

- DevOps: Docker (compose), GitHub (actions), Azure VPS,
- Backend: UV, Python, FastAPI, MySQL
- Frontend: React, Chakra (perhaps), TypeScript, Bun

### Pre-Requirements

- Docker Engine
- Docker Compose
- Bun

Also remember to populate a .env in the backend. Use .env.example

## NEW Usage Guidelines (3 Steps!)

1. Create .env file in /backend from the .env.example

Don't change any values unless you intend to manually create a different user for the database.

2. Build and run the 3 containers with docker compose.

from the root folder:

```bat
docker compose -f docker-compose.dev.yml up -d
```

Your should now have these 3 containers running

| Container       | Port |
| :-------------- | :--: |
| Backend Server  | 8000 |
| Frontend Server | 3000 |
| MySQL 8.4       | 3306 |

3. Create schema + tables + triggers + functions + procedures

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

You are probably using Docker Compose V1. Use docker-compose instead

```bash
docker-compose -f docker-compose.dev.yml up -d
```

2. Internal Server Error:

Probably you just build a new container and now need to populate \
your database

3. \[Insert a lot of different python errors here\] \

Try and make sure all the python libraries are correctly \
installed. (only relevant when working with the files locally \
and not inside the docker container mentioned above)

```bash
cd backend
uv sync
```

## This these top-tier advice not work for you?

Contact Wenmin Ye for free technical support support
