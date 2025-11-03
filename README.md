# GameTable
This application is developed for the courses "Full Stack Development", "Databases for Developers", and "Testing"  on the first semester of the PBa Software Development Top-up

## Stack
DevOps: Docker (compose), GitHub (actions), Azure VPS,
Backend: UV, Python, FastAPI, MySQL
Frontend: React, Chakra (perhaps), TypeScript

### Pre-Requirements
Docker Engine
Docker Compose
UV
A MySQL Database

Also remember to populate a .env in the backend. Use .env.example

To run the backend application change dir to /backend and then:
```bash
uv run --env-file .env -- uvicorn app.main:app --port 8000 --reload
```

Install the dependancies for the backend application
```bash
cd backend/
uv sync
```

```

```bash

```
