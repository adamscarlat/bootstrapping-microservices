import environment

from fastapi import Depends, FastAPI, HTTPException, Response
from motor.motor_asyncio import AsyncIOMotorDatabase
from flixtube_common.cosmosdb.db_operations import CosmosDbOperations

app = FastAPI()

cosmos_ops = CosmosDbOperations(
  environment.DBHOST, 
  environment.DB_USERNAME, 
  environment.DB_PASSWORD,
  "video-streaming"
)

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