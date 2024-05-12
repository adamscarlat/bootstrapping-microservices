import asyncio
import json
import environment
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection, AsyncIOMotorClient

def get_database_client():
  mongo_uri = f"mongodb://{environment.DB_USERNAME}:{environment.DB_PASSWORD}@{environment.DBHOST}:{environment.DBPORT}"
  print (mongo_uri)
  client = AsyncIOMotorClient(mongo_uri)
  database = client[environment.DBNAME]
  
  return database
  
def seed_db():
  database: AsyncIOMotorDatabase = get_database_client()
  with open("db-fixture/videos.json") as f:
    data = json.load(f)
  
  collection = database.get_collection("videos")
  if collection == None:
    asyncio.run(database.create_collection("videos"))

  database["videos"].insert_many(data)
  
  print (data)

def clean_db():
  database: AsyncIOMotorDatabase = get_database_client()
  with open("db-fixture/videos.json") as f:
    data = json.load(f)
  
  database.drop_collection("videos")
  database.drop_collection("history")


