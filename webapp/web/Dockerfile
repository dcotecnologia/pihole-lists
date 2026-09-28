FROM oven/bun:1
WORKDIR /app
ADD package.json bun.lock ./
RUN bun install --frozen-lockfile
ADD . .
EXPOSE 5173
CMD ["bun", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]
