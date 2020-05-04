import asyncio

from aiokafka import AIOKafkaProducer


async def init_kafka_producer(app):
    config = app['config']
    loop = asyncio.get_event_loop()
    producer = AIOKafkaProducer(
        loop=loop,
        bootstrap_servers=config['KAFKA_SERVERS'],
        api_version=config['KAFKA_API_VERSION'],
    )
    await producer.start()
    app['kafka_producer'] = producer


async def stop_kafka_producer(app):
    producer = app['kafka_producer']
    if producer:
        await producer.stop()
