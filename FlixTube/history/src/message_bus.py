from aiormq import connect
from environment import RABBIT_USER, RABBIT_PASSWORD, RABBIT_HOST, RABBIT_PORT

async def consume_queue(queue_name, callback):
    rabbit_url = f"amqp://{RABBIT_USER}:{RABBIT_PASSWORD}@{RABBIT_HOST}:{RABBIT_PORT}"
    connection = await connect(url=rabbit_url)
    channel = await connection.channel()
    await channel.queue_declare(queue=queue_name)

    await channel.basic_consume(
        queue=queue_name,
        consumer_callback=callback,
        no_ack=True
    )  
