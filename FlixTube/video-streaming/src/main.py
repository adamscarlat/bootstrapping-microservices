import io
from fastapi import Depends, FastAPI, HTTPException, Response
from fastapi.responses import RedirectResponse
from starlette.responses import StreamingResponse
from video import download_video, send_viewed_message
from motor.motor_asyncio import AsyncIOMotorDatabase

import environment
import db

app = FastAPI()

@app.get("/video")
async def redirect_to_url(id: str, db_client: AsyncIOMotorDatabase = Depends(db.get_database_client)):
  item = await db.get_item_by_id(db_client, "videos", id)
  if not item or "videoPath" not in item:
     raise HTTPException(status_code=404, detail="Item not found")
  
  video_path = item["videoPath"]

  await send_viewed_message(id, video_path)

  return RedirectResponse(url=f"/video/download?path={video_path}")

@app.get("/video/download")
async def stream_video(path: str):
  video_response = await download_video(path)

  return StreamingResponse(
      io.BytesIO(video_response.content), 
      media_type="video/mp4",
      headers={
        "Content-Length": str(video_response.headers["Content-Length"])
      }
  )

if __name__ == "__main__":
  environment.start_app()