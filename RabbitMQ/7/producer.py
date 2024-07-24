import pika

# Direct exchange is for when you want a exact match between exchange name and queue name.

def send_message():
    # Establish connection with RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare a direct exchange named 'direct_logs'
    channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

    # Message and routing key
    routing_key = 'info'
    message = 'Hello World!'

    # Publish the message to the 'direct_logs' exchange with the routing key 'info'
    channel.basic_publish(exchange='direct_logs', routing_key=routing_key, body=message)
    print(f" [x] Sent {message} with routing key '{routing_key}'")

    # Close the connection
    connection.close()

if __name__ == "__main__":
    send_message()
