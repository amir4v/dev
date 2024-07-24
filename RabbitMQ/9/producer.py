import pika

def send_message(routing_key, message):
    # Establish connection with RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare a topic exchange named 'topic_logs'
    channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

    # Publish the message to the 'topic_logs' exchange with the specified routing key
    channel.basic_publish(exchange='topic_logs', routing_key=routing_key, body=message)
    print(f" [x] Sent '{message}' with routing key '{routing_key}'")

    # Close the connection
    connection.close()

if __name__ == "__main__":
    # Example messages with different routing keys
    send_message('kern.info', 'A kernel info message')
    send_message('auth.warn', 'An auth warning message')
    send_message('cron.error', 'A cron error message')
