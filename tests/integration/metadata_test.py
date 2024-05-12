import json
import httpx
import pytest
from db import db_fixture_path

@pytest.mark.asyncio
async def test_get_videos():
  url = "http://localhost:8004/videos"
  async with httpx.AsyncClient() as client:
    response = await client.get(url)
    assert response.status_code == 200

    with open(db_fixture_path) as f:
      expected_data = json.load(f)

    actual_data = json.loads(response.content)["videos"]

    assert len(actual_data) == len(expected_data)

    for expected_item in expected_data:
      actual_item = list(filter(lambda d: d["id"] == expected_item["id"], actual_data))[0]
      assert actual_item["videoPath"] == expected_item["videoPath"]


