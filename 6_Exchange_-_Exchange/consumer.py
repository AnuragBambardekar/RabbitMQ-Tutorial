import pika
from pika.exchange_type import ExchangeType

def on_message_received(ch, method, properties, body):
    print(f"Received new message: {body}")

connection_parameters = pika.ConnectionParameters('localhost')

# create a connection
connection = pika.BlockingConnection(connection_parameters)

# create a default channel
channel = connection.channel()

# declare the second exchange
channel.exchange_declare(exchange='secondExchange', exchange_type=ExchangeType.fanout)

# declare a queue
channel.queue_declare(queue='letterbox')

# bind the queue
channel.queue_bind('letterbox', 'secondExchange')

channel.basic_consume(queue='letterbox', auto_ack=True, on_message_callback=on_message_received)

print("Started consuming messages...")
channel.start_consuming()
