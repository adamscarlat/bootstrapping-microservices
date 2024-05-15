import json

from fastapi.testclient import TestClient
from src.main import app
from src.main import cosmos_ops
from mocks.mock_db_client import MockCollection, MockDbClient


async def mock_get_database_client():
    print ("HERE: mock_get_database_client")
    videos = [{
        "id": "1",
        "videoPath" : "SampleVideo_1280x720_5mb.mp4"
    }]
    mock_collection = MockCollection(videos)
    mock_collections_map = {
       "videos": mock_collection
    }
    return MockDbClient(mock_collections_map)

app.dependency_overrides[cosmos_ops.get_database_client] = mock_get_database_client
client = TestClient(app)

def test_get_videos():
  response = client.get("/videos")
  videos = json.loads(response.content)["videos"]
  video = videos[0]

  assert video["id"] == "1" and video["videoPath"] == "SampleVideo_1280x720_5mb.mp4"
