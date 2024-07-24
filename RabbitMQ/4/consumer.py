import pika

def receive_message():
    # Establish connection with RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare a queue named 'hello'
    channel.queue_declare(queue='hello')

    # Callback function to handle the received message
    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")

    # Subscribe to the 'hello' queue
    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    # Start consuming
    channel.start_consuming()

if __name__ == "__main__":
    receive_message()
