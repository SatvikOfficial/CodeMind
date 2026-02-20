from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_security_headers_present() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
