import pika

def receive_message(headers_match):
    # Establish connection with RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare a headers exchange named 'headers_logs'
    channel.exchange_declare(exchange='headers_logs', exchange_type='headers')

    # Declare a temporary queue with a random name
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    # Bind the queue to the 'headers_logs' exchange with the specified header match
    channel.queue_bind(exchange='headers_logs', queue=queue_name, arguments=headers_match)

    print(f" [*] Waiting for messages matching headers {headers_match}. To exit press CTRL+C")

    # Callback function to handle the received message
    def callback(ch, method, properties, body):
        print(f" [x] Received '{body}' with headers {properties.headers}")

    # Subscribe to the queue
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    # Start consuming
    channel.start_consuming()

if __name__ == "__main__":
    # Example header matches
    headers_match = {'x-match': 'all', 'format': 'pdf', 'type': 'report'}
    receive_message(headers_match)
