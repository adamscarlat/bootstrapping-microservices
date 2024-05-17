import environment
from flixtube_common.cosmosdb.db_operations import CosmosDbOperations

cosmos_ops = CosmosDbOperations(
  environment.DBHOST, 
  environment.DB_USERNAME, 
  environment.DB_PASSWORD,
  "video-streaming"
)

class UploadedVideoMessage:
  video_path: str

async def handle_uploaded_message(message: UploadedVideoMessage):
  video_path = message["video_path"]
  async for db_client in cosmos_ops.get_database_client():

    collection = db_client.get_collection("videos")

    document = await collection.find_one({"videoPath": video_path})
    if document:
      print (f"Video with path: {video_path} already exists. Ignoring...")
      return

    print (f"Saving video metadata with path: {video_path}...")
    doc_count = await collection.count_documents({})
    await collection.insert_one({
       "id": str(doc_count + 1),
       "videoPath": video_path
    })