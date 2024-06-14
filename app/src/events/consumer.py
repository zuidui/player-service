import aio_pika
from aio_pika import connect_robust, IncomingMessage
from aio_pika.exceptions import ConnectionClosed, ChannelClosed
import json
import asyncio

from service.team_service import TeamService

from utils.logger import logger_config
from utils.config import get_settings

log = logger_config(__name__)
settings = get_settings()

consumer_instance = None


class Consumer:
    def __init__(
        self,
        connection: aio_pika.abc.AbstractRobustConnection,
        queue_name: str = settings.QUEUE_NAME,
    ):
        self.queue_name = queue_name
        self.connection = connection
        self.channel = None
        self.queue = None

    async def connect(self):
        self.channel = await self.connection.channel()
        self.queue = await self.channel.declare_queue(self.queue_name, durable=True)

    async def consume(self):
        while True:
            try:
                await self.queue.consume(self._callback, no_ack=False)
                log.info(f"Starting to consume messages from {self.queue_name}")
                break
            except (ConnectionClosed, ChannelClosed) as e:
                log.error(f"Connection closed, retrying... {e}")
                await asyncio.sleep(5)
                await self.connect()

    async def _callback(self, message: IncomingMessage):
        async with message.process():
            try:
                message_data = json.loads(message.body.decode("utf-8"))
                log.info(f"Received message: {message_data}")
                await TeamService.handle_message(message_data)
            except json.JSONDecodeError as e:
                log.error(
                    f"Failed to decode message: {message.body.decode('utf-8')} - Error: {e}"
                )

    async def close(self):
        if self.connection:
            await self.connection.close()
            log.info("Connection closed")


async def start_consumer(loop) -> Consumer:
    connection = await connect_robust(
        host=settings.BROKER_HOST, 
        port=settings.BROKER_PORT, 
        loop=loop,
        heartbeat=settings.BROKER_HEARTBEAT,
        connection_attempts=settings.BROKER_CONNECTION_ATTEMPTS,
        connection_timeout=settings.BROKER_CONNECTION_TIMEOUT,
        attempt_delay=settings.BROKER_ATTEMPT_DELAY,
    )
    consumer = Consumer(connection)
    await consumer.connect()
    asyncio.create_task(consumer.consume())  # Ensure consume runs in the background
    return consumer
