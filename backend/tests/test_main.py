import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db

# 1. Gunakan SQLite in-memory khusus untuk Unit Testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 2. Override dependency get_db FastAPI agar menggunakan DB SQLite sementara
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# 3. Setup fixture untuk membuat tabel SQLite sebelum test dan hapus setelah test
@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

# 4. Test Cases
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "backend"}

def test_create_and_read_task():
    # Test POST /api/v1/tasks
    payload = {"title": "Test Task CI/CD", "description": "Testing with SQLite"}
    response = client.post("/api/v1/tasks", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task CI/CD"
    assert "id" in data

    # Test GET /api/v1/tasks
    response_get = client.get("/api/v1/tasks")
    assert response_get.status_code == 200
    assert len(response_get.json()) == 1