import json
import os


config = dict()

config['HOST'] = os.getenv('HOST', '0.0.0.0')
config['PORT'] = int(os.getenv('PORT', 8080))

# config['KAFKA_API_VERSION'] = '0.10.2'
config['KAFKA_API_VERSION'] = 'auto'

KAFKA_SERVERS = json.loads(os.getenv('KAFKA_SERVERS', '[]'))
if not KAFKA_SERVERS:
    # KAFKA_SERVERS = [
    #     '192.168.10.8:9092',
    #     '192.168.10.9:9092',
    #     '192.168.10.10:9092'
    # ]
    # KAFKA_SERVERS = '127.0.0.1:9092'
    KAFKA_SERVERS = '192.168.1.102:32782'

config['KAFKA_SERVERS'] = KAFKA_SERVERS

