FROM python:3.14-slim


ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=/app

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./

RUN uv pip install --system .

COPY . .

RUN mkdir -p /app/logs

CMD ["python", "-m","scripts.run_all_migrations.py"]
