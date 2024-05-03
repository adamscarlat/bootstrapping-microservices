import environment

from fastapi import FastAPI
from storage import create_blob_service_client, stream_blob
from starlette.responses import StreamingResponse

app = FastAPI()

# http://0.0.0.0:8001/video?path=SampleVideo_1280x720_5mb.mp4
@app.get("/video")
async def get_video(path: str):
    container_name = "videos"
    blob_service_client = create_blob_service_client()
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(path)
    
    video_properties = blob_client.get_blob_properties()

    return StreamingResponse(
        stream_blob(blob_client),
        media_type="video/mp4",
        headers={
            "Content-Length": str(video_properties.size)
        }
    )

if __name__ == "__main__":
  environment.start_app()
