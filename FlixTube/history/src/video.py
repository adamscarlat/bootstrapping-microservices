import json
import db

async def process_queue_viewed_message(message):
  data = json.loads(message.body)

  print (f"Received message: {data}. Processing...")

  async for db_client in db.get_database_client():
    await db.save_item(db_client, "history", data)




  