FROM python:3.12-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:0.9.6 /uv /uvx /bin/

# Install the application dependencies.
WORKDIR /app

# Copy dependencies lock file and .env
COPY ./backend/pyproject.toml ./backend/uv.lock ./backend/.env ./

# Install dependencies
RUN uv sync --locked

# Copy the application into the container.
COPY ./backend/ /app

# remove any accidentally included virtualenv
RUN rm -rf /app/.venv

# Run the application.
CMD ["uv", "run", "--env-file", ".env","--", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
