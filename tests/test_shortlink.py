import json
import tempfile
import os
import pytest
from shortlink import create_app

@pytest.fixture
def client(tmp_path):
    db_file = tmp_path / "test_links.db"
    app = create_app(db_path=str(db_file))
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c

def test_create_and_idempotent(client):
    resp = client.post("/links", json={"url": "https://google.com"})
    assert resp.status_code == 201
    body = resp.get_json()
    assert "code" in body and body["url"] == "https://google.com"

    resp2 = client.post("/links", json={"url": "https://google.com"})
    assert resp2.status_code == 200
    assert resp2.get_json()["code"] == body["code"]

def test_follow_and_count(client):
    r = client.post("/links", json={"url": "https://google.com"})
    code = r.get_json()["code"]

    follow = client.get(f"/{code}")
    assert follow.status_code == 302

    stats = client.get(f"/links/{code}/stats")
    assert stats.status_code == 200
    assert stats.get_json()["clicks"] == 1

def test_bad_url_and_unknown_code(client):
    r = client.post("/links", json={"url": "not a url"})
    assert r.status_code == 400
    assert r.get_json()["error"] == "validation_failed"

    missing = client.get("/links/doesnotexist/stats")
    assert missing.status_code == 404