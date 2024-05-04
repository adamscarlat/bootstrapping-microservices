import json
import aio_pika
import environment

class PikaClient:
  def __init__(self, process_callable, queue_name, loop): 
    self.process_callable = process_callable
    self.queue_name = queue_name
    self.loop = loop
    
  async def consume(self):
    """Setup message listener with the current running loop"""

    connection = await aio_pika.connect_robust(
      host=environment.RABBIT_HOST,
      port=environment.RABBIT_PORT,
      login=environment.RABBIT_USER,
      password=environment.RABBIT_PASSWORD,
      loop=self.loop
    )

    channel = await connection.channel()
    queue = await channel.declare_queue(self.queue_name)
    await queue.consume(self.process_incoming_message, no_ack=False)
    
    print ('Established pika async listener')
    
    return connection
  
  async def process_incoming_message(self, message):
    """Processing incoming message from RabbitMQ"""
    
    body = message.body
    print ('Received message')
    
    if body:
      await self.process_callable(json.loads(body))

    await message.ack()