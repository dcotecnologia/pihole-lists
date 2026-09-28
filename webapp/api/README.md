# Pi-hole Lists API

A small FastAPI app that reads/writes the curated lists under `../../lists`
(mounted as `LISTS_DIR`, default `/app/lists`). Standalone from the main
project's `src/` pipeline - it only touches the same `lists/*.txt` files, no
shared Python path.

Local-only tool: no authentication. Don't expose these ports beyond your own
machine/LAN.

## Run

Via the root `docker-compose.yml` (recommended, hot reload included):

```sh
docker compose up api
```

Or locally:

```sh
uv sync
LISTS_DIR=../../lists uv run uvicorn app.main:app --reload
```

## Test

```sh
uv run pytest -q
```

## Endpoints

- `GET /api/lists` - every list's name and entry count
- `POST /api/lists` `{"name": "..."}` - create an empty list
- `DELETE /api/lists/{name}` - delete a list
- `GET /api/lists/{name}/items?query=&page=&page_size=` - paginated,
  substring-filtered entries
- `POST /api/lists/{name}/items` `{"domain": "..."}` - add an entry
- `DELETE /api/lists/{name}/items/{domain}` - remove an entry

Interactive docs at `/docs` while the app is running.
