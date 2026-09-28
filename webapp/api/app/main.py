"""FastAPI app exposing CRUD over the curated lists in `LISTS_DIR`.

Run locally: `uv run uvicorn app.main:app --reload`.
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app import lists_repo
from app.schemas import AddItemRequest, CreateListRequest, ListItemsPage, ListSummary

app = FastAPI(title="Pi-hole Lists API")

# Local-only tool (see .claude/SECURITY.md): CORS is wide open on purpose,
# there is no auth layer, and it must never be exposed beyond localhost/LAN.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/lists", response_model=list[ListSummary])
def get_lists():
    return lists_repo.list_lists()


@app.post("/api/lists", response_model=ListSummary, status_code=201)
def post_list(body: CreateListRequest):
    try:
        lists_repo.create_list(body.name)
    except lists_repo.InvalidNameError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except lists_repo.ListAlreadyExistsError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return {"name": body.name, "item_count": 0}


@app.delete("/api/lists/{name}", status_code=204)
def delete_list(name: str):
    try:
        lists_repo.delete_list(name)
    except lists_repo.InvalidNameError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except lists_repo.ListNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/api/lists/{name}/items", response_model=ListItemsPage)
def get_items(name: str, query: str = "", page: int = Query(1, ge=1), page_size: int = Query(50, ge=1, le=500)):
    try:
        return lists_repo.get_items(name, query=query, page=page, page_size=page_size)
    except lists_repo.InvalidNameError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except lists_repo.ListNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/api/lists/{name}/items", status_code=201)
def post_item(name: str, body: AddItemRequest):
    try:
        added = lists_repo.add_item(name, body.domain)
    except lists_repo.InvalidNameError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except lists_repo.ListNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"added": added}


@app.delete("/api/lists/{name}/items/{domain}", status_code=200)
def delete_item(name: str, domain: str):
    try:
        removed = lists_repo.remove_item(name, domain)
    except lists_repo.InvalidNameError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except lists_repo.ListNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"removed": removed}
