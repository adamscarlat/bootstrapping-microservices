import json
import aio_pika

from aio_pika import ExchangeType, Message, DeliveryMode

class PikaClient:
  def __init__(self, loop, host, port, username, password): 
    self.loop = loop
    self.host = host
    self.port = port
    self.username = username
    self.password = password
    
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

  async def consume_exchange(self, exchange_name: str, process_callable, exchange_type = ExchangeType.FANOUT):
    connection = await self.get_connection()
    channel = await connection.channel()

    exchange = await channel.declare_exchange(exchange_name, exchange_type)
    
    # Creates an anonymous queue that gets destroyed when this process exits
    queue = await channel.declare_queue(exclusive=True)
    await queue.bind(exchange)

    self.process_callable = process_callable
    await queue.consume(self.process_incoming_message, no_ack=False)

    print (f'Established pika async listener - exchange connection: {exchange_name} of type: {exchange_type}')

  async def process_incoming_message(self, message):
    """Processing incoming message from RabbitMQ"""
    
    body = message.body
    print ('Received message')
    
    if body:
      await self.process_callable(json.loads(body))

    await message.ack()

  async def get_connection(self):
    return await aio_pika.connect_robust(
      host=self.host,
      port=self.port,
      login=self.username,
      password=self.password,
      loop=self.loop
    )

  def get_message_bytes(self, message):
    return bytes(json.dumps(message), encoding="utf-8")


