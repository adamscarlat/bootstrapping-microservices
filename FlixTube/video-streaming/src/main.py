import io
from fastapi import FastAPI
from starlette.responses import StreamingResponse
from video import download_video

import environment

app = FastAPI()

@app.get("/video")
async def stream_video():
  video_name = "SampleVideo_1280x720_5mb.mp4"
  video_response = await download_video(video_name)

  return StreamingResponse(
      io.BytesIO(video_response.content), 
      media_type="video/mp4",
      headers={
        "Content-Length": str(video_response.headers["Content-Length"])
      }
  )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=environment.PORT)