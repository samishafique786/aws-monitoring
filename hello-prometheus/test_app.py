import pytest
from app import app

@pytest.fixture
def client():
    # Flask provides a test client for unit testing
    with app.test_client() as client:
        yield client

def test_hello_endpoint(client):
    """Test that the / endpoint returns 'hello world'"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.data == b"hello world"

def test_metrics_endpoint(client):
    """Check /metrics output"""
    response = client.get("/metrics")
    assert response.status_code == 200
    # Print the raw metrics output
    print(response.data.decode("utf-8"))
    # Check that our histogram metric exists
    assert b'hello_world_request_latency_seconds' in response.data
