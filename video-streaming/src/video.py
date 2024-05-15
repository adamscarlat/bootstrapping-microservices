import asyncio
import os
import environment
import httpx

from flixtube_common.rabbitmq.pika_client import PikaClient

def get_file_size(path: str):
  return os.path.getsize(path)

# Function to read video file as bytes
def stream_file(path: str):
  with open(path, mode='rb') as file:
    while True:
      chunk = file.read(1024)
      if not chunk:
        break
      yield chunk

def read_file(path: str):
  with open(path, mode='rb') as file:
    return file.read()


async def download_video(video_name: str):
  video_storage_url = f"http://{environment.VIDEO_STORAGE_HOST}:{environment.VIDEO_STORAGE_PORT}/video"
  print (f"video_storage_url:  {video_storage_url}")
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

async def publish_viewed_message(id: str, video_path: str, exchange_name: str = "", queue_name: str = ""):
  loop = asyncio.get_running_loop()
  pika_client = PikaClient(
    loop, 
    environment.RABBIT_HOST, 
    environment.RABBIT_PORT,
    environment.RABBIT_USER,
    environment.RABBIT_PASSWORD
  )

  message = {
    "id": id,
    "video_path": video_path
  }

  if queue_name:
    await pika_client.send_direct(message, queue_name)
    return
  
  await pika_client.send_to_exchange(message, exchange_name)