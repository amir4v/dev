# docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:alpine
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
import pika

def send_message():
    # Establish connection with RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare a queue named 'hello'
    channel.queue_declare(queue='hello')

    # Publish a message to the 'hello' queue
    channel.basic_publish(exchange='',
                          routing_key='hello',
                          body='Hello World!')
    print(" [x] Sent 'Hello World!'")

    # Close the connection
    connection.close()

if __name__ == "__main__":
    send_message()
# -----------------------------------------------------------------------------
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
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
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
# -----------------------------------------------------------------------------
import pika

def subscribe():
    # Establish connection with RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare a 'fanout' exchange named 'logs'
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
    subscribe()
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
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
# -----------------------------------------------------------------------------
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
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
import pika

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
# -----------------------------------------------------------------------------
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
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
import pika

def send_message():
    # Establish connection with RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare a fanout exchange named 'logs'
    channel.exchange_declare(exchange='logs', exchange_type='fanout')

    # Message to be published
    message = 'Hello World!'

    # Publish the message to the 'logs' exchange
    channel.basic_publish(exchange='logs', routing_key='', body=message)
    print(f" [x] Sent {message}")

    # Close the connection
    connection.close()

if __name__ == "__main__":
    send_message()
# -----------------------------------------------------------------------------
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
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
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
# -----------------------------------------------------------------------------
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
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
import pika

def send_message(headers, message):
    # Establish connection with RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare a headers exchange named 'headers_logs'
    channel.exchange_declare(exchange='headers_logs', exchange_type='headers')

    # Publish the message to the 'headers_logs' exchange with the specified headers
    channel.basic_publish(exchange='headers_logs', routing_key='', body=message, properties=pika.BasicProperties(headers=headers))
    print(f" [x] Sent '{message}' with headers {headers}")

    # Close the connection
    connection.close()

if __name__ == "__main__":
    # Example messages with different headers
    send_message({'format': 'pdf', 'type': 'report'}, 'PDF Report')
    send_message({'format': 'doc', 'type': 'report'}, 'DOC Report')
    send_message({'format': 'pdf', 'type': 'invoice'}, 'PDF Invoice')
# -----------------------------------------------------------------------------
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
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
