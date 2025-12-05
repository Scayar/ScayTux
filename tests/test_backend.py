"""
TUX Droid AI Control - Backend Tests
====================================

Basic tests for the FastAPI backend.
"""

import pytest
from fastapi.testclient import TestClient

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    from backend.main import app
    return TestClient(app)


class TestHealthEndpoints:
    """Tests for health and status endpoints."""
    
    def test_root_endpoint(self, client):
        """Test root endpoint returns API info."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert data["name"] == "TUX Droid AI Control API"
    
    def test_health_endpoint(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "tux_connected" in data
    
    def test_status_endpoint(self, client):
        """Test status endpoint."""
        response = client.get("/status")
        assert response.status_code == 200
        data = response.json()
        assert "connected" in data
        assert "driver_type" in data


class TestTuxEndpoints:
    """Tests for TUX control endpoints."""
    
    def test_eyes_blink(self, client):
        """Test eyes blink endpoint."""
        response = client.post("/tux/eyes", json={
            "action": "blink",
            "count": 3
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert data["action"] == "blink_eyes"
    
    def test_eyes_open(self, client):
        """Test eyes open endpoint."""
        response = client.post("/tux/eyes", json={"action": "open"})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
    
    def test_mouth_move(self, client):
        """Test mouth move endpoint."""
        response = client.post("/tux/mouth", json={
            "action": "move",
            "count": 2
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
    
    def test_wings_wave(self, client):
        """Test wings wave endpoint."""
        response = client.post("/tux/wings", json={
            "action": "wave",
            "count": 3,
            "speed": 4
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
    
    def test_spin_left(self, client):
        """Test spin left endpoint."""
        response = client.post("/tux/spin", json={
            "action": "left",
            "angle": 4,
            "speed": 3
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
    
    def test_leds_on(self, client):
        """Test LEDs on endpoint."""
        response = client.post("/tux/leds", json={
            "action": "on",
            "target": "both"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
    
    def test_sound_play(self, client):
        """Test sound play endpoint."""
        response = client.post("/tux/sound", json={
            "action": "play",
            "sound_number": 0,
            "volume": 100
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
    
    def test_sleep(self, client):
        """Test sleep endpoint."""
        response = client.post("/tux/sleep", json={
            "action": "sleep",
            "mode": "normal"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
    
    def test_wake_up(self, client):
        """Test wake up endpoint."""
        response = client.post("/tux/sleep", json={"action": "wake"})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
    
    def test_custom_action(self, client):
        """Test custom action endpoint."""
        response = client.post("/tux/custom", json={
            "action_type": "blink_eyes",
            "params": {"count": 5}
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
    
    def test_invalid_action(self, client):
        """Test invalid action returns error."""
        response = client.post("/tux/custom", json={
            "action_type": "invalid_action",
            "params": {}
        })
        assert response.status_code == 400


class TestConnectionEndpoints:
    """Tests for connection endpoints."""
    
    def test_connect(self, client):
        """Test connect endpoint."""
        response = client.post("/tux/connect")
        assert response.status_code == 200
        data = response.json()
        assert "success" in data
    
    def test_disconnect(self, client):
        """Test disconnect endpoint."""
        response = client.post("/tux/disconnect")
        assert response.status_code == 200
        data = response.json()
        assert "success" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

