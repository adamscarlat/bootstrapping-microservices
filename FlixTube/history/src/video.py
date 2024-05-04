import json
import db
from models import ViewedVideoMessage

async def save_viewed_message(message: ViewedVideoMessage):
  async for db_client in db.get_database_client():
    await db.save_item(db_client, "history", message)  
