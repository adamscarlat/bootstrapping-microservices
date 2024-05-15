from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_video_streaming_microservice():
    response = client.get("/video/test")
    assert response.status_code == 200