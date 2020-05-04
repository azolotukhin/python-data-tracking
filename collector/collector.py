import asyncio
import json
import time

from aiokafka import AIOKafkaConsumer

from settings import config


async def produce(loop, queue, topic, group_id):
    try:
        print(f'Connecting to Kafka topic {topic}.')
        consumer = AIOKafkaConsumer(
            topic,
            loop=loop,
            bootstrap_servers=config['KAFKA_SERVERS'],
            api_version=config['KAFKA_API_VERSION'],
            group_id=group_id
        )
        print('Starting producer')
        await consumer.start()

        print('Starting to consume from Kafka queue')
        async for msg in consumer:
            try:
                message = json.loads(msg.value.decode('utf-8'))
                data = message.get('data')

                print(f'Added one record to local queue {queue.qsize()} / {queue.maxsize}')
                await queue.put(data)
            except Exception as e:
                print(e)
                await asyncio.sleep(0.01)

        await consumer.stop()
    except:
        print('Unhandled error during kafka (de)connection')
        raise


async def store_bulk(to_store):
    print(f'Some logic for insert to DB {len(to_store)}')


async def consume(loop, queue, batch_size=50000, batch_max_time=300):
    last_stored_time = time.time()
    while True:
        if queue.qsize() > batch_size or time.time() - last_stored_time > batch_max_time:
            print(f'Start consume {queue.qsize()}')
            to_store = []
            while not queue.empty():
                to_store.append(await queue.get())
            try:
                await store_bulk(to_store)
            except Exception as e:
                print(f'Consumer: DB down, try to reconnect {e}')
                break
            last_stored_time = time.time()
        await asyncio.sleep(0.01)
    print('I am out of infinite loop.')
