import pika

def send_message():
    # Establish connection with RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare a queue named 'hello'
    channel.queue_declare(queue='-hello-') # Declaring the queue. / Ensures that the queue exists.

    # Publish a message to the 'hello' queue
    channel.basic_publish(exchange='', # Do not do any special exchanges and just send them to the queue.
                          routing_key='hello', # Specifies the queue. (allows wildcard pattern)
                          body='Hello World!')
    print(" [x] Sent 'Hello World!'")

    # Close the connection
    connection.close()

if __name__ == "__main__":
    send_message()
