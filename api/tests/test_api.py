import os
import pytest
from fastapi.testclient import TestClient

os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["ADMIN_USERNAME"] = "admin"
os.environ["ADMIN_PASSWORD"] = "admin"

from api.main import app
from api.deps import init_db


@pytest.fixture(autouse=True)
def setup_db():
    # Recreate tables in the in‑memory SQLite for each test
    init_db()
    yield


def test_health():
    client = TestClient(app)
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_list_tournaments_empty():
    client = TestClient(app)
    resp = client.get("/tournaments")
    assert resp.status_code == 200
    assert resp.json() == []
