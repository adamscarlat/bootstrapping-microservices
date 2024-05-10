import environment
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection, AsyncIOMotorClient


async def get_database_client():
  mongo_uri = f"mongodb://{environment.DB_USERNAME}:{environment.DB_PASSWORD}@{environment.DBHOST}"
  client = AsyncIOMotorClient(mongo_uri)
  database = client[environment.DBNAME]
  
  yield database
  
  client.close()

def get_collection(db_client: AsyncIOMotorDatabase, collection_name: str) -> AsyncIOMotorCollection:
  return db_client.get_collection(collection_name)

async def get_item_by_id(db_client: AsyncIOMotorDatabase, collection_name: str, item_id: str):
  collection = get_collection(db_client, collection_name)
  item = await collection.find_one({"id": item_id})

  return item

async def save_item(db_client: AsyncIOMotorDatabase, collection_name: str, item: dict):
  collection = get_collection(db_client, collection_name)
  saved = await collection.insert_one(item)

  return saved


