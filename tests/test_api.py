"""
Tests for the FastAPI application.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import create_app

@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    app = create_app()
    return TestClient(app)

def test_root_endpoint(client):
    """Test the root endpoint returns the HTML file."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_websocket_connection(client):
    """Test WebSocket connection."""
    with client.websocket_connect("/ws") as websocket:
        # Should receive welcome message
        data = websocket.receive_json()
        assert "Welcome to the WebSocket server!" in data["data"]
        assert data["client"] == "server"
