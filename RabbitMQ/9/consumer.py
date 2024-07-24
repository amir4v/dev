import pika

def receive_message(binding_keys):
    # Establish connection with RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare a topic exchange named 'topic_logs'
    channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

    # Declare a temporary queue with a random name
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    # Bind the queue to the 'topic_logs' exchange with the specified binding keys
    for binding_key in binding_keys:
        channel.queue_bind(exchange='topic_logs', queue=queue_name, routing_key=binding_key)

    print(f" [*] Waiting for messages matching {binding_keys}. To exit press CTRL+C")

    # Callback function to handle the received message
    def callback(ch, method, properties, body):
        print(f" [x] Received {body} with routing key '{method.routing_key}'")

    # Subscribe to the queue
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    # Start consuming
    channel.start_consuming()

if __name__ == "__main__":
    # Example binding keys
    binding_keys = ['kern.*', '*.error']
    receive_message(binding_keys)
