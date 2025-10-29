# Backend Application for GameTable

Made with UV, FastAPI, MySQL,

## Full stack

### Frontend: LINK TO FRONTEND

React, TypeScript, Chakra (perhaps)

### Backend

FastAPI, UV, MySQL
Pydantic, SqlAlchemy (ORM), RUFF

#### DB and ORM

Pydantic (as alternative to Dataclasses)
SqlAlchemy (ORM)

#### Dev Environment

Docker, Docker Compose
UV.lock is kept in VSC

## Setup

Clone repo

```bash
git clone https://github.com/davijoe/GameTable
```

Install python libs via UV sync from the backend dir

```bash
cd GameTable/backend
uv sync
```

Remember to set database auth info in .env
And in the temp url in db.py
