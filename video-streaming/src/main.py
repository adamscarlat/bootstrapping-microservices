import environment

from fastapi import Depends, FastAPI, HTTPException, Response
from fastapi.responses import RedirectResponse
from video import download_video, publish_viewed_message, read_file
from motor.motor_asyncio import AsyncIOMotorDatabase
from flixtube_common.cosmosdb.db_operations import CosmosDbOperations

app = FastAPI()

cosmos_ops = CosmosDbOperations(
  environment.DBHOST, 
  environment.DB_USERNAME, 
  environment.DB_PASSWORD,
  "video-streaming"
)

@app.get("/video")
async def redirect_to_url(id: str, db_client: AsyncIOMotorDatabase = Depends(cosmos_ops.get_database_client)):
  item = await cosmos_ops.get_item_by_id(db_client, "videos", id)
  if not item or "videoPath" not in item:
     raise HTTPException(status_code=404, detail="Item not found")
  
  video_path = item["videoPath"]
  await publish_viewed_message(id, item["videoPath"], exchange_name="viewed")

  return RedirectResponse(url=f"/video/download?path={video_path}")

@app.get("/video/download")
async def stream_video(path: str):
  video_response = await download_video(path)

  return Response(
    content=video_response.content, 
    media_type="video/mp4",
    headers={
      "Content-Length": str(video_response.headers["Content-Length"])
    }
  )

@app.get("/video/test")
async def stream_test_video():

  video_bytes = read_file("./videos/SampleVideo_1280x720_5mb.mp4")

  return Response(
    content=video_bytes, 
    media_type="video/mp4",
    headers={
      "Content-Length": str(len(video_bytes))
    }
  )

if __name__ == "__main__":
  environment.start_app()