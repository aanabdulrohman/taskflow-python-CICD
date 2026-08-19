import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, Testing if hasattr(app.database, 'Testing') else None

# Setup tabel SQLite sebelum test dan hapus setelah test selesai
@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "backend"}

def test_create_and_read_task():
    # Test POST /api/v1/tasks
    payload = {"title": "CI/CD Test Task", "description": "Testing with SQLite"}
    response = client.post("/api/v1/tasks", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "CI/CD Test Task"
    assert "id" in data

    # Test GET /api/v1/tasks
    response_get = client.get("/api/v1/tasks")
    assert response_get.status_code == 200
    assert len(response_get.json()) == 1