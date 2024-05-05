import asyncio
from contextlib import asynccontextmanager

import environment

from fastapi import FastAPI
from pika_client import PikaClient


async def placeholder_callback(msg):
  await asyncio.sleep(0)
  print(f"RECS: MESSAGE RECEIVED: {msg}")
  

@asynccontextmanager
async def lifespan(_: FastAPI):
    loop = asyncio.get_running_loop()

    pika_client = PikaClient(placeholder_callback, loop)
    task = loop.create_task(pika_client.consume_exchange("viewed"))
    await task

    yield

app = FastAPI(lifespan=lifespan)

@app.get("/recommendations")
async def get_history():
  return "hello recommendations!"

if __name__ == "__main__":
  environment.start_app()