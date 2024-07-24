import pika

def send_message():
    # Establish connection with RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare a queue named 'hello'
    channel.queue_declare(queue='hello')

    # Message to be published
    message = 'Hello World!'

    # Publish the message to the 'hello' queue via the default exchange
    channel.basic_publish(exchange='', routing_key='hello', body=message)
    print(f" [x] Sent {message}")

    # Close the connection
    connection.close()

if __name__ == "__main__":
    send_message()
