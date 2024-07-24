import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)

channel = connection.channel()

channel.queue_declare(queue='greeting', durable=False)

def callback(ch, method, props, body):
    print(body.decode())
    print(body.count(b'.'))
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print('[*] Received.')

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='greeting', on_message_callback=callback)

channel.start_consuming()
