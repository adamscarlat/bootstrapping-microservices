import asyncio
import os
import environment
import httpx

from pika_client import PikaClient

def get_file_size(path: str):
  return os.path.getsize(path)

# Function to read video file as bytes
def stream_video_file(video_path: str):
  with open(video_path, mode='rb') as video_file:
    while True:
      chunk = video_file.read(1024)
      if not chunk:
        break
      yield chunk

async def download_video(video_name: str):
  video_storage_url = f"http://{environment.VIDEO_STORAGE_HOST}:{environment.VIDEO_STORAGE_PORT}/video"
  async with httpx.AsyncClient() as client:
    return await client.get(video_storage_url, params={
       "path": video_name
    })
  
async def send_viewed_message(video_id: str, video_path: str):
  history_url = f"http://{environment.HISTORY_HOST}:{environment.HISTORY_PORT}/viewed"
  data = {
    "id": video_id,
    "video_path": video_path
  }
  async with httpx.AsyncClient() as client:
    await client.post(history_url, json=data)

async def publish_viewed_message(id: str, video_path: str):
  loop = asyncio.get_running_loop()
  pika_client = PikaClient("viewed", loop)

  await pika_client.send_message({
    "id": id,
    "video_path": video_path
  })