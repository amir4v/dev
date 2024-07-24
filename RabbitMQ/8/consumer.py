import pika

def receive_message():
    # Establish connection with RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare a fanout exchange named 'logs'
    channel.exchange_declare(exchange='logs', exchange_type='fanout')

    # Declare a temporary queue with a random name
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    # Bind the queue to the 'logs' exchange
    channel.queue_bind(exchange='logs', queue=queue_name)

    print(' [*] Waiting for messages. To exit press CTRL+C')

    # Callback function to handle the received message
    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")

    # Subscribe to the queue
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    # Start consuming
    channel.start_consuming()

if __name__ == "__main__":
    receive_message()
