from contextlib import asynccontextmanager
import environment
import db
import video

from fastapi import FastAPI, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from models import ViewedVideoMessage
from message_bus import consume_queue

@asynccontextmanager
async def lifespan(_: FastAPI):
    await consume_queue("viewed", video.process_queue_viewed_message)
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