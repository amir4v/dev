import pika

"""
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:alpine
"""

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)

channel = connection.channel()

channel.queue_declare('greeting')

def callback(ch, method, props, body):
    print(f"""
    [ch]: {ch},\n
    [method]: {method},\n
    [props]: {props},\n
    [body]: {body},\n
    """)
    print('[*] Received.')

channel.basic_consume(
    queue='greeting',
    on_message_callback=callback,
    auto_ack=True
)

channel.start_consuming()
