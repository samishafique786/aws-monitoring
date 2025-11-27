import pytest
from app import app

@pytest.fixture
def client():

    with app.test_client() as client:
        yield client

def test_hello_endpoint(client):
    """Test that the / endpoint returns 'hello world'"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.data == b"hello world"

def test_metrics_endpoint(client):
    """Test that the /metrics endpoint returns Prometheus metrics"""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert b'hello_world_request_seconds' in response.data  # thiss will check that our histogram metric exists
    assert response.headers["Content-Type"] == "text/plain; version=0.0.4; charset=utf-8"
