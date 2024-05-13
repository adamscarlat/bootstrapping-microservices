import asyncio
from contextlib import asynccontextmanager

from aio_pika import ExchangeType
import environment
import db
import video

from fastapi import FastAPI, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from models import ViewedVideoMessage
from pika_client import PikaClient


@asynccontextmanager
async def lifespan(_: FastAPI):
    loop = asyncio.get_running_loop()
    pika_client = PikaClient(video.save_viewed_message, loop)
    task = loop.create_task(pika_client.consume_exchange("viewed"))
    await task

    yield

app = FastAPI(lifespan=lifespan)

@app.get("/history")
async def get_history(db_client: AsyncIOMotorDatabase = Depends(db.get_database_client)):
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
                      db_client: AsyncIOMotorDatabase = Depends(db.get_database_client)):
  #print (data)
  data_dict = data.model_dump()
  saved = await db.save_item(db_client, "history", data_dict)

if __name__ == "__main__":
  environment.start_app()