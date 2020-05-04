import asyncio

import click

from collector.collector import produce, consume


@click.group()
def cli():
    pass


@cli.command('collector')
@click.option('--kafka-group-id', 'kafka_group_id', type=click.STRING, help='Kafka Group ID', required=False)
@click.option('--kafka-topic', 'kafka_topic', type=click.STRING, help='Kafka Topic Inbox', required=False)
@click.option('--source-type', 'source_type', type=click.STRING, help='Events Source Type', required=False)
@click.option('--batch_size', 'batch_size', type=click.INT, help='Max Events for consume', required=False, default=50000)
@click.option('--batch_max_time', 'batch_max_time', type=click.INT, help='Consume Period', required=False, default=300)
def collector(kafka_group_id, kafka_topic, source_type, batch_size, batch_max_time):
    loop = asyncio.get_event_loop()
    queue = asyncio.Queue(maxsize=50)
    asyncio.ensure_future(produce(loop, queue, kafka_topic, kafka_group_id))
    asyncio.ensure_future(consume(loop, queue, batch_size, batch_max_time))
    loop.run_forever()
    loop.close()
    print('Consumer finished.')
