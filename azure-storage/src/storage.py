import asyncio
import environment
import io

from typing import IO
from azure.storage.blob import BlobServiceClient, BlobClient
from flixtube_common.rabbitmq.pika_client import PikaClient

def create_blob_service_client():
  blob_service_client = BlobServiceClient(
    account_url=f"https://{environment.STORAGE_ACCOUNT_NAME}.blob.core.windows.net",
    credential=environment.STORAGE_ACCESS_KEY
  )
  return blob_service_client

def download_blob(blob_client: BlobClient):
  blob_data = blob_client.download_blob()
  return blob_data.readall()

def stream_blob(blob_client: BlobClient):
  blob_data = blob_client.download_blob()
  stream: IO[bytes] = io.BytesIO()
  blob_data.readinto(stream)

  stream.seek(0)

  return stream

async def publish_uploaded_message(video_path: str, exchange_name: str = "", queue_name: str = ""):
  loop = asyncio.get_running_loop()
  pika_client = PikaClient(
    loop, 
    environment.RABBIT_HOST, 
    environment.RABBIT_PORT,
    environment.RABBIT_USER,
    environment.RABBIT_PASSWORD
  )

  message = {
    "video_path": video_path
  }

  if queue_name:
    await pika_client.send_direct(message, queue_name)
    return
  
  await pika_client.send_to_exchange(message, exchange_name)