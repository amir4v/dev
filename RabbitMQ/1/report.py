import uuid
import json

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

queue = channel.queue_declare('order_report')
queue_name = queue.method.queue

channel.queue_bind(
    exchange='order',
    queue=queue_name,
    routing_key='order.report',
)


def callback(ch, method, properties, body):
    payload = json.loads(body)
    print(f"""
    id: {payload.get('id')}
    name: {payload.get('name')}
    """)
    print(f"[*] Notifying {payload['name']}")
    print('[*] Done')
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(on_message_callback=callback, queue=queue_name)

print('[*] Waiting for notify a message.')

channel.start_consuming()
