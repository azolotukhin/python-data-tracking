from aiohttp import web

from endpoint.kafka_utils import init_kafka_producer, stop_kafka_producer
from endpoint.views import send_event
from settings import config


app = web.Application()
app.router.add_get('/send_event', send_event)
# app.router.add_post('/send_event', send_event)
app['config'] = config
app.on_startup.append(init_kafka_producer)
app.on_cleanup.append(stop_kafka_producer)

if __name__ == '__main__':
    web.run_app(app, host=config['HOST'], port=config['PORT'])
