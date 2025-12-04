FROM oven/bun:1 AS dev

WORKDIR /app

# Copy only deps
COPY package.json bun.lock ./

RUN bun install

EXPOSE 3000

CMD ["bun", "run", "dev", "--","--host", "0.0.0.0", "--port", "3000"]
