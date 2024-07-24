import pika

def receive_message():
    # Establish connection with RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare a direct exchange named 'direct_logs'
    channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

    # Declare a queue named 'hello'
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    # Bind the queue to the 'direct_logs' exchange with the routing key 'info'
    routing_key = 'info'
    channel.queue_bind(exchange='direct_logs', queue=queue_name, routing_key=routing_key)

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
