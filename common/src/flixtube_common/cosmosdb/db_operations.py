from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection, AsyncIOMotorClient

class CosmosDbOperations:
  def __init__(self, 
          uri: str,
          username: str,
          password: str,
          db_name: str     
        ) -> None:
    self.uri = uri
    self.username = username
    self.password = password
    self.db_name = db_name

  async def get_database_client(self):
    mongo_uri = f"mongodb://{self.username}:{self.password}@{self.uri}"
    client = AsyncIOMotorClient(mongo_uri)
    database = client[self.db_name]
    
    yield database
    
    client.close()

  def get_collection(self, db_client: AsyncIOMotorDatabase, collection_name: str) -> AsyncIOMotorCollection:
    return db_client.get_collection(collection_name)

  async def get_item_by_id(self, db_client: AsyncIOMotorDatabase, collection_name: str, item_id: str):
    collection = self.get_collection(db_client, collection_name)
    item = await collection.find_one({"id": item_id})

    return item
  
  async def save_item(self, db_client: AsyncIOMotorDatabase, collection_name: str, item: dict):
    collection = self.get_collection(db_client, collection_name)
    saved = await collection.insert_one(item)

    return saved  