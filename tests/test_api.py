import pytest
from fastapi.testclient import TestClient
from src.backend.app import app
import io

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["status"] == "ok"

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True

def test_chat_audio_no_file():
    response = client.post("/chat_audio")
    assert response.status_code == 422

def test_transcribe_no_file():
    response = client.post("/transcribe")
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_chat_audio_with_mock_file():
    # Create mock audio file
    audio_content = b"fake audio content"
    files = {"file": ("test.wav", io.BytesIO(audio_content), "audio/wav")}
    
    # This will fail due to invalid audio, but tests the endpoint structure
    response = client.post("/chat_audio", files=files)
    assert response.status_code in [400, 500]  # Expected to fail with mock data