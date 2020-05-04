import datetime
import json

from aiohttp import web
from google.protobuf import json_format


async def send_event(request):
    kafka_producer = request.app['kafka_producer']
    # data = await request.json()
    # print(data)
    data = [
        {
            'kafka_topic': 'test',
            'data': {
                'player_id': '111111',
                'level': 10
            }
        }
    ] * 50
    for event in data:
        topic = 'test'
        event['datetime'] = datetime.datetime.utcnow().isoformat()
        message = bytes(json.dumps(event), 'utf-8')
        await kafka_producer.send(topic, message)
    return web.Response(status=200)
