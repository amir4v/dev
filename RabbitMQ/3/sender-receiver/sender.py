import pika

"""
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:alpine
"""

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)

channel = connection.channel()

channel.queue_declare('greeting')

channel.basic_publish(
    exchange='',
    routing_key='greeting',
    body='Hello :)',
)

print('[*] Sent Hello :) message!')

connection.close()

print('[*] Connection closed.')
