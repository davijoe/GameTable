FROM python:3.12-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:0.9.6 /uv /uvx /bin/

# Install the application dependencies.
WORKDIR /app

# Copy dependencies lock file and .env
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --locked

# Copy the application into the container.
COPY . /app

# Run the application.
CMD ["uv", "run", "--env-file", ".env","--", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
