import asyncio
import httpx
import pytest
import db

@pytest.mark.asyncio
async def test_stream_video():
  video_streaming_port = 8000
  url = f"http://localhost:{video_streaming_port}/video?id=1"
  async with httpx.AsyncClient() as client:
    stream_response = await client.get(url)

    # Redirect
    assert stream_response.status_code == 307

    # Wait for async bus message to settle
    await asyncio.sleep(1)

    database = db.get_database_client()
    history_collection = database.get_collection("history")
    history_items = await history_collection.find({}).to_list(length=None)
    
    assert len(history_items) == 1

    history_item = history_items[0]
    assert history_item["id"] == "1"
    assert history_item["video_path"] == "SampleVideo_1280x720_5mb.mp4"

    redirect_location = stream_response.headers["Location"]
    redirect_url = f"http://localhost:{video_streaming_port}{redirect_location}"
    print (redirect_url)
    download_response = await client.get(redirect_url)
    assert download_response.status_code == 200
    