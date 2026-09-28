import pytest
from fastapi.testclient import TestClient

from app import lists_repo
from app.main import app


@pytest.fixture(autouse=True)
def lists_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(lists_repo, "LISTS_DIR", tmp_path)
    return tmp_path


@pytest.fixture
def client():
    return TestClient(app)


def test_health(client):
    assert client.get("/api/health").json() == {"status": "ok"}


def test_create_list_get_lists_add_item_get_items(client):
    resp = client.post("/api/lists", json={"name": "example"})
    assert resp.status_code == 201

    resp = client.get("/api/lists")
    assert resp.json() == [{"name": "example", "item_count": 0}]

    resp = client.post("/api/lists/example/items", json={"domain": "a.example"})
    assert resp.status_code == 201
    assert resp.json() == {"added": True}

    resp = client.get("/api/lists/example/items")
    assert resp.json()["items"] == ["a.example"]


def test_create_list_conflict(client):
    client.post("/api/lists", json={"name": "dup"})
    resp = client.post("/api/lists", json={"name": "dup"})
    assert resp.status_code == 409


def test_create_list_invalid_name(client):
    resp = client.post("/api/lists", json={"name": "../etc"})
    assert resp.status_code == 422


def test_delete_list(client):
    client.post("/api/lists", json={"name": "todelete"})
    resp = client.delete("/api/lists/todelete")
    assert resp.status_code == 204
    assert client.get("/api/lists").json() == []


def test_delete_list_not_found(client):
    resp = client.delete("/api/lists/missing")
    assert resp.status_code == 404


def test_get_items_not_found(client):
    resp = client.get("/api/lists/missing/items")
    assert resp.status_code == 404


def test_add_item_not_found(client):
    resp = client.post("/api/lists/missing/items", json={"domain": "a.example"})
    assert resp.status_code == 404


def test_add_item_invalid_domain(client):
    client.post("/api/lists", json={"name": "example"})
    resp = client.post("/api/lists/example/items", json={"domain": "not a domain"})
    assert resp.status_code == 422


def test_delete_item(client):
    client.post("/api/lists", json={"name": "example"})
    client.post("/api/lists/example/items", json={"domain": "a.example"})

    resp = client.delete("/api/lists/example/items/a.example")
    assert resp.json() == {"removed": True}

    resp = client.delete("/api/lists/example/items/a.example")
    assert resp.json() == {"removed": False}


def test_delete_item_list_not_found(client):
    resp = client.delete("/api/lists/missing/items/a.example")
    assert resp.status_code == 404
