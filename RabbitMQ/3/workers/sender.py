import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)
channel = connection.channel()

channel.queue_declare(queue='greeting', durable=False)

channel.basic_publish(
    exchange='',
    routing_key='greeting',
    body='Hello :)',
    properties=pika.BasicProperties(delivery_mode=2),
)

print('[*] Sent.')

connection.close()
