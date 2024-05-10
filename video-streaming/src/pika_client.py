import json
import aio_pika
import environment

from aio_pika import ExchangeType, Message, DeliveryMode

class PikaClient:
  def __init__(self, loop): 
    self.loop = loop
    
  async def send_direct(self, message: dict, queue_name: str):
    connection = await self.get_connection()
    channel = await connection.channel()

    exchange = channel.default_exchange
    
    message_bytes = self.get_message_bytes(message)
    await exchange.publish(
      message=Message(body=message_bytes),
      routing_key=queue_name
    )

    await connection.close()
  
  async def send_to_exchange(self, message: dict, 
                             exchange_name: str, 
                             exchange_type = ExchangeType.FANOUT):
    connection = await self.get_connection()
    channel = await connection.channel()

    exchange = await channel.declare_exchange(exchange_name, exchange_type)
    message_bytes = self.get_message_bytes(message)
    message_wrapped = Message(
      body=message_bytes,
      delivery_mode=DeliveryMode.PERSISTENT
    )

    await exchange.publish(
      message=message_wrapped,
      routing_key = "",
    )

    await connection.close()


  async def get_connection(self):
    return await aio_pika.connect_robust(
      host=environment.RABBIT_HOST,
      port=environment.RABBIT_PORT,
      login=environment.RABBIT_USER,
      password=environment.RABBIT_PASSWORD,
      loop=self.loop
    )

  def get_message_bytes(self, message):
    return bytes(json.dumps(message), encoding="utf-8")


