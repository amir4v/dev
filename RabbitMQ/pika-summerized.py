# ALL
import pika

# ALL
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# ALL
channel.exchange_declare(exchange='NAME', exchange_type='direct') # declare
channel.exchange_declare(exchange='NAME', exchange_type='fanout') # declare
channel.exchange_declare(exchange='NAME', exchange_type='topic') # declare
channel.exchange_declare(exchange='NAME', exchange_type='headers') # declare

# -----------------------------------------------------------------------------

# PRODUCER (and maybe CONSUMER so ALL)
channel.queue_declare(queue='NAME') # declare

# PRODUCER
channel.basic_publish(exchange='', routing_key='ROUTING-KEY', body=message) # default, direct
channel.basic_publish(exchange='NAME', routing_key='', body=message) # fanout
channel.basic_publish(exchange='NAME', routing_key='ROUTING-KEY', body=message) # topic
channel.basic_publish(exchange='NAME', routing_key='', body=message, properties=pika.BasicProperties(headers=headers)) # headers

# -----------------------------------------------------------------------------

# CONSUMER
result = channel.queue_declare(queue='', exclusive=True) # declare
queue_name = result.method.queue

# CONSUMER
channel.queue_bind(exchange='NAME', queue=queue_name) # fanout
channel.queue_bind(exchange='NAME', queue=queue_name, routing_key=routing_key) # direct, topic
channel.queue_bind(exchange='NAME', queue=queue_name, arguments=headers_match) # headers

# CONSUMER
def callback(ch, method, properties, body):
    pass

# CONSUMER
channel.basic_consume(queue='NAME', on_message_callback=callback, auto_ack=True)
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

# CONSUMER
channel.start_consuming()

# -----------------------------------------------------------------------------

# ALL
connection.close()
