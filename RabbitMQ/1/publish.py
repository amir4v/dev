import uuid
import json

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(
    exchange='order',
    exchange_type='direct',
)

data = {
    'id': str(uuid.uuid4()),
    'name': 'Amir',
}

channel.basic_publish(
    exchange='order',
    routing_key='order.notify',
    body=json.dumps({'name': data['name'],}),
)
print('[*] Sent notify message')

channel.basic_publish(
    exchange='order',
    routing_key='order.report',
    body=json.dumps(data),
)
print('[*] Sent data message')

connection.close()
