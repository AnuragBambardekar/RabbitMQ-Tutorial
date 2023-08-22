import pika
from pika.exchange_type import ExchangeType

def alt_queue_on_message_received(ch, method, properties, body):
    print(f"Alternate Exchange Received new message: {body}")

def main_queue_on_message_received(ch, method, properties, body):
    print(f"Main Exchange Received new message: {body}")

connection_parameters = pika.ConnectionParameters('localhost')

# create a connection
connection = pika.BlockingConnection(connection_parameters)

# create a default channel
channel = connection.channel()

# declare alt exchange and main exchange
channel.exchange_declare(exchange='altexchange', exchange_type=ExchangeType.fanout)
channel.exchange_declare(exchange='mainexchange', exchange_type=ExchangeType.direct,
                         arguments={'alternate-exchange':'altexchange'})

# declare an altexchange queue
channel.queue_declare(queue='altexchangequeue')
channel.queue_bind('altexchangequeue', 'altexchange')
channel.basic_consume(queue='altexchangequeue', auto_ack=True, on_message_callback=alt_queue_on_message_received)

# declare a mainexchange queue
channel.queue_declare(queue='mainexchangequeue')
channel.queue_bind('mainexchangequeue', 'mainexchange', 'test')
channel.basic_consume(queue='mainexchangequeue', auto_ack=True, on_message_callback=main_queue_on_message_received)

print("Started consuming messages...")
channel.start_consuming()
