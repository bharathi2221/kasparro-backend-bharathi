from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_get_data_endpoint():
    response = client.get("/data")

    assert response.status_code == 200

    body = response.json()
    assert "request_id" in body
    assert "latency_ms" in body
    assert "data" in body
    assert isinstance(body["data"], list)
