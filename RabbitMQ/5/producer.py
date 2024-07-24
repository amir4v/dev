import pika

def publish_message():
    # Establish connection with RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare a 'fanout' exchange named 'logs'
    channel.exchange_declare(exchange='logs', exchange_type='fanout')

    # Message to be published
    message = 'Hello World!'

    # Publish the message to the 'logs' exchange
    channel.basic_publish(exchange='logs', routing_key='', body=message)
    print(f" [x] Sent {message}")

    # Close the connection
    connection.close()

if __name__ == "__main__":
    publish_message()
