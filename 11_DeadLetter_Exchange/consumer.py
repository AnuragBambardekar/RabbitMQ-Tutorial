import pika
from pika.exchange_type import ExchangeType

def main_queue_on_message_received(ch, method, properties, body):
    print(f"Main Exchange Received new message: {body}")

def dlx_queue_on_message_received(ch, method, properties, body):
    print(f"DLX Received new message: {body}")

connection_parameters = pika.ConnectionParameters('localhost')

# create a connection
connection = pika.BlockingConnection(connection_parameters)

# create a default channel
channel = connection.channel()

# declare and main exchange
channel.exchange_declare(exchange='mainexchange', exchange_type=ExchangeType.direct)
channel.exchange_declare(exchange='dlx', exchange_type=ExchangeType.fanout)

# declare a mainexchange queue
"""
Delete the mainexchangequeue from RabbitMQ console if it already exists.
"""
channel.queue_declare(queue='mainexchangequeue', arguments={'x-dead-letter-exchange':'dlx', 'x-message-ttl':1000})
channel.queue_bind('mainexchangequeue', 'mainexchange', 'test')
# channel.basic_consume(queue='mainexchangequeue', auto_ack=True, on_message_callback=main_queue_on_message_received)

# declare a dlx queue
channel.queue_declare(queue='dlxqueue')
channel.queue_bind('dlxqueue', 'dlx')
channel.basic_consume(queue='dlxqueue', auto_ack=True, on_message_callback=dlx_queue_on_message_received)

print("Started consuming messages...")
channel.start_consuming()
