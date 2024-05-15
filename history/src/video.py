import environment
from flixtube_common.cosmosdb.db_operations import CosmosDbOperations
from models import ViewedVideoMessage

cosmos_ops = CosmosDbOperations(
  environment.DBHOST, 
  environment.DB_USERNAME, 
  environment.DB_PASSWORD,
  "video-streaming"
)

async def save_viewed_message(message: ViewedVideoMessage):
  async for db_client in cosmos_ops.get_database_client():
    await cosmos_ops.save_item(db_client, "history", message)  
