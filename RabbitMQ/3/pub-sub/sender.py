import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)

channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

message = 'Hello :)'

channel.basic_publish(exchange='logs', routing_key='', body=message)

connection.close()
