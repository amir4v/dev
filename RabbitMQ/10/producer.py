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
