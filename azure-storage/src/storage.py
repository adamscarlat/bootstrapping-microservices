import environment
import io

from typing import IO
from azure.storage.blob import BlobServiceClient, BlobClient

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