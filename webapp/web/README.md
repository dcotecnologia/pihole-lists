# Pi-hole Lists Web

A small Vue 3 + Vite SPA to browse, search, add, and remove entries in the
curated lists via `../api`.

## Run

Via the root `docker-compose.yml` (recommended, hot reload included):

```sh
docker compose up web
```

Open **<http://localhost:8098>** - not 5173. Vite listens on 5173 _inside_
the container; `docker-compose.yml` publishes that as `8098` on the host
(`"8098:5173"`), since 8080/8090 were already taken on this machine.

Or locally (no Docker - this one really does listen on 5173):

```sh
bun install
VITE_API_BASE_URL=http://localhost:8000/api bun run dev
```

## Build

```sh
bun run build
```

`VITE_API_BASE_URL` defaults to `/api` (same-origin), meant to be proxied to
the `api` service by whatever serves the built `dist/`.
