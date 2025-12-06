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

def test_new_metrics(client):
    """Test that new standard metrics are generated"""
    # Make a request to trigger metrics
    client.get("/")
    
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.data.decode("utf-8")
    
    # Check for new metrics
    assert 'http_requests_total' in data
    assert 'http_request_duration_seconds' in data
    assert 'active_requests' in data
    assert 'app_info' in data
    
    # Check specific label existence (partial match)
    assert 'method="GET"' in data
    assert 'endpoint="/"' in data
    assert 'status="200"' in data
    assert 'version="1.0.0"' in data
