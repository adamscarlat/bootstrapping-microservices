from fastapi import FastAPI
from starlette.responses import StreamingResponse

import environment

from models.item import Item
from video import get_file_size, stream_video_file

app = FastAPI()

@app.get("/video")
async def stream_video():
  video_path = "videos/SampleVideo_1280x720_5mb.mp4"
  file_size_bytes = get_file_size(video_path)

  return StreamingResponse(
     stream_video_file(video_path), 
     media_type="video/mp4",
     headers={
        "Content-Length": str(file_size_bytes)
     }
  )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=environment.PORT)