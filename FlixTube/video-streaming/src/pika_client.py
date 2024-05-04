import json
import aio_pika
import environment

class PikaClient:
  def __init__(self, queue_name, loop, exchange = ""): 
    self.queue_name = queue_name
    self.loop = loop
    self.exchange = exchange
    
  async def send_message(self, message: dict):
    connection = await aio_pika.connect_robust(
      host=environment.RABBIT_HOST,
      port=environment.RABBIT_PORT,
      login=environment.RABBIT_USER,
      password=environment.RABBIT_PASSWORD,
      loop=self.loop
    )

    channel = await connection.channel()

    if self.exchange == "":
      exchange = channel.default_exchange
    else:
      exchange = await channel.get_exchange(self.exchange)
    
    message_bytes = bytes(json.dumps(message), encoding="utf-8")
    await exchange.publish(
      message=aio_pika.Message(body=message_bytes),
      routing_key=self.queue_name
    )

    await connection.close()
