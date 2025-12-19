import os
import json
import sys
from pathlib import Path
# ensure project root is on sys.path for imports
sys.path.append(str(Path(__file__).resolve().parents[1]))
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def setup_tmp_storage(tmp_path, monkeypatch):
    # use sqlite for tests
    dbfile = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///" + str(dbfile))
    monkeypatch.setenv("USE_SQLITE", "1")
    # initialize DB
    from app import db
    db.init_db()
    return str(dbfile)


def test_auth_enforced(tmp_path, monkeypatch):
    setup_tmp_storage(tmp_path, monkeypatch)
    res = client.post("/api/v1/playlists", json={"name": "x", "tracks": []})
    assert res.status_code == 403


def test_crud_workflow(tmp_path, monkeypatch):
    setup_tmp_storage(tmp_path, monkeypatch)
    # use demo key
    headers = {"X-API-KEY": "demo_api_key"}

    create = client.post("/api/v1/playlists", json={"name": "My List", "tracks": []}, headers=headers)
    assert create.status_code == 201
    data = create.json()
    pid = data["id"]

    get = client.get(f"/api/v1/playlists/{pid}")
    assert get.status_code == 200

    update = client.put(f"/api/v1/playlists/{pid}", json={"name": "Updated", "tracks": []}, headers=headers)
    assert update.status_code == 200
    assert update.json()["name"] == "Updated"

    delete = client.delete(f"/api/v1/playlists/{pid}", headers=headers)
    assert delete.status_code == 204
