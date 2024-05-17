import asyncio
import environment
import upload_handler

from fastapi import Depends, FastAPI, HTTPException, Response
from motor.motor_asyncio import AsyncIOMotorDatabase
from flixtube_common.cosmosdb.db_operations import CosmosDbOperations
from contextlib import asynccontextmanager
from flixtube_common.rabbitmq.pika_client import PikaClient


cosmos_ops = CosmosDbOperations(
  environment.DBHOST, 
  environment.DB_USERNAME, 
  environment.DB_PASSWORD,
  "video-streaming"
)

@asynccontextmanager
async def lifespan(_: FastAPI):
    loop = asyncio.get_running_loop()
    pika_client = PikaClient(
       loop,
       environment.RABBIT_HOST,
       environment.RABBIT_PORT,
       environment.RABBIT_USER,
       environment.RABBIT_PASSWORD
    )
    task = loop.create_task(pika_client.consume_exchange("uploaded", upload_handler.handle_uploaded_message))
    await task

    yield

app = FastAPI(lifespan=lifespan)

@app.get("/videos")
async def get_videos(db_client: AsyncIOMotorDatabase = Depends(cosmos_ops.get_database_client)):
  fields = {"_id": 0, "id": 1, "videoPath": 1}
  
  videos_collection = cosmos_ops.get_collection(db_client, "videos").find({}, projection=fields)
  videos = await videos_collection.to_list(length=None)

  print (videos)

  return {"videos": videos}

@app.get("/test")
async def get_videos():
  return "hello"

if __name__ == "__main__":
  environment.start_app()