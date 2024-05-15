import environment

from fastapi import Depends, FastAPI, HTTPException, Response, UploadFile, File, Request
from storage import create_blob_service_client, download_blob
from motor.motor_asyncio import AsyncIOMotorDatabase
from azure.core.exceptions import ResourceExistsError
from flixtube_common.cosmosdb.db_operations import CosmosDbOperations

cosmos_ops = CosmosDbOperations(
  environment.DBHOST, 
  environment.DB_USERNAME, 
  environment.DB_PASSWORD,
  "video-streaming"
)

app = FastAPI()

# http://0.0.0.0:8001/video?path=SampleVideo_1280x720_5mb.mp4
@app.get("/video")
async def get_video(path: str):
    container_name = "videos"
    blob_service_client = create_blob_service_client()
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(path)
    
    video_properties = blob_client.get_blob_properties()
    video_bytes = download_blob(blob_client)

    return Response(
       content=video_bytes, 
       media_type="application/octet-stream",
       headers={
        "Content-Length": str(video_properties.size)
       }
    )

@app.post("/upload")
async def post_video(request: Request, db_client: AsyncIOMotorDatabase = Depends(cosmos_ops.get_database_client)):
  form = await request.form()
  
  contents = form["file"].file.read()

  file_name = form["fileName"]

  container_name = "videos"
  blob_service_client = create_blob_service_client()
  container_client = blob_service_client.get_container_client(container_name)
  blob_client = container_client.get_blob_client(file_name)

  try:
    blob_client.upload_blob(contents)
  except ResourceExistsError as e:
    raise HTTPException(status_code=409, detail="Item with the same name already exists")

  collection = db_client.get_collection("videos")
  doc_count = await collection.count_documents({})
  await collection.insert_one({
     "id": str(doc_count + 1),
     "videoPath": file_name
  })

  return {"uploadComplete": True}


if __name__ == "__main__":
  environment.start_app()
