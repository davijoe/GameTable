FROM oven/bun:1 AS dev

WORKDIR /app

COPY frontend/package.json frontend/bun.lock ./

RUN bun install

COPY ./frontend /app

EXPOSE 3000

CMD ["bun", "run", "dev", "--","--host", "0.0.0.0", "--port", "3000"]
