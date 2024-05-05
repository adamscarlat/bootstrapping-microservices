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
async def get_history():
  return "hello computer!"

@app.post("/viewed")
async def post_viewed(data: ViewedVideoMessage, 
                      db_client: AsyncIOMotorDatabase = Depends(db.get_database_client)):
  #print (data)
  data_dict = data.model_dump()
  saved = await db.save_item(db_client, "history", data_dict)

if __name__ == "__main__":
  environment.start_app()