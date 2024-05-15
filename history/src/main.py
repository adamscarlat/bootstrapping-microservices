import asyncio
from contextlib import asynccontextmanager

import environment
import video

from fastapi import FastAPI, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from models import ViewedVideoMessage
from flixtube_common.cosmosdb.db_operations import CosmosDbOperations
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
    task = loop.create_task(pika_client.consume_exchange("viewed", video.save_viewed_message))
    await task

    yield

app = FastAPI(lifespan=lifespan)

@app.get("/history")
async def get_history(db_client: AsyncIOMotorDatabase = Depends(cosmos_ops.get_database_client)):
  fields = {"_id": 0, "id": 1, "video_path": 1}

  history_items = await db_client.get_collection("history").find(projection=fields).to_list(length=None)
  
  history_counts = {}
  for item in history_items:
     if item["id"] not in history_counts:
        history_counts[item["id"]] = 0
     history_counts[item["id"]] += 1

  counted_items = []
  for id in history_counts.keys():
     for item in history_items:
        if item["id"] == id:
           item["count"] = history_counts[id]
           counted_items.append(item)
           break
  
  print (counted_items)

  return {
     "history": counted_items
  }
  

@app.post("/viewed")
async def post_viewed(data: ViewedVideoMessage, 
                      db_client: AsyncIOMotorDatabase = Depends(cosmos_ops.get_database_client)):
  #print (data)
  data_dict = data.model_dump()
  saved = await cosmos_ops.save_item(db_client, "history", data_dict)

if __name__ == "__main__":
  environment.start_app()