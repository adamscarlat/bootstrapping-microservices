import json
import aio_pika
import environment

from aio_pika import ExchangeType

class PikaClient:
  def __init__(self, process_callable, loop): 
    self.process_callable = process_callable
    self.loop = loop
    
  async def consume_direct(self, queue_name):
    """Setup message listener with the current running loop"""

    connection = await self.get_connection()
    channel = await connection.channel()
    queue = await channel.declare_queue(queue_name)
    await queue.consume(self.process_incoming_message, no_ack=False)
    
    print (f'Established pika async listener - direct connection to queue: {queue_name}')
    
    return connection

  async def consume_exchange(self, exchange_name: str, exchange_type = ExchangeType.FANOUT):
    connection = await self.get_connection()
    channel = await connection.channel()

    exchange = await channel.declare_exchange(exchange_name, exchange_type)
    
    # Creates an anonymous queue that gets destroyed when this process exits
    queue = await channel.declare_queue(exclusive=True)
    await queue.bind(exchange)
    await queue.consume(self.process_incoming_message, no_ack=False)

    print (f'Established pika async listener - exchange connection: {exchange_name} of type: {exchange_type}')

  async def get_connection(self):
    connection = await aio_pika.connect_robust(
      host=environment.RABBIT_HOST,
      port=environment.RABBIT_PORT,
      login=environment.RABBIT_USER,
      password=environment.RABBIT_PASSWORD,
      loop=self.loop
    )

    return connection

  async def process_incoming_message(self, message):
    """Processing incoming message from RabbitMQ"""
    
    body = message.body
    print ('Received message')
    
    if body:
      await self.process_callable(json.loads(body))

    await message.ack()