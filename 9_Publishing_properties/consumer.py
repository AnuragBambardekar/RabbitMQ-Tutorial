import pika
from pika.exchange_type import ExchangeType

def callback(ch, method, properties, body):
    print(f"Received message: {body}")

connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.exchange_declare(exchange='pubsub', exchange_type=ExchangeType.fanout)

# Ensure the queue is durable and bound to the exchange
channel.queue_declare(queue='test', durable=True)
channel.queue_bind(exchange='pubsub', queue='test')

# Set up the callback function to handle incoming messages
channel.basic_consume(queue='test', on_message_callback=callback, auto_ack=True)

print('Waiting for messages. To exit, press CTRL+C')
channel.start_consuming()
