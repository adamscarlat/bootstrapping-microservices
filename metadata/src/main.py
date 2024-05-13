import environment
import db

from fastapi import Depends, FastAPI, HTTPException, Response
from motor.motor_asyncio import AsyncIOMotorDatabase


app = FastAPI()

@app.get("/videos")
async def get_videos(db_client: AsyncIOMotorDatabase = Depends(db.get_database_client)):
  fields = {"_id": 0, "id": 1, "videoPath": 1}
  
  videos_collection = db.get_collection(db_client, "videos").find({}, projection=fields)
  videos = await videos_collection.to_list(length=None)

  print (videos)

  return {"videos": videos}

@app.get("/test")
async def get_videos():
  return "hello"

if __name__ == "__main__":
  environment.start_app()