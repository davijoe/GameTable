FROM python:3.14-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml .

RUN uv pip install --system -r pyproject.toml

COPY . .

RUN mkdir -p /app/logs

CMD ["python", "scripts/run_all_migrations.py"]