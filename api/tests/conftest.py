import pytest
from fastapi.testclient import TestClient

from api.app.main import app


@pytest.fixture(scope="session")
def client():
    """FastAPI test client (shared for all tests in the session)."""
    with TestClient(app) as c:
        yield c


@pytest.fixture
def sample_texts():
    """Sample texts for indexing tests."""
    return [
        "Python is a programming language",
        "Docker is a containerization platform",
        "Kubernetes orchestrates containers",
    ]


@pytest.fixture
def sample_metadata():
    """Sample metadata for indexing tests."""
    return [
        {"topic": "programming", "language": "python"},
        {"topic": "devops", "tool": "docker"},
        {"topic": "devops", "tool": "kubernetes"},
    ]
