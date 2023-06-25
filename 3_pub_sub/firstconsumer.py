import pika
from pika.exchange_type import ExchangeType

def on_message_received(ch, method, properties, body):
    print(f"FirstConsumer: Received new message: {body}")

connection_params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_params)

channel = connection.channel()

channel.exchange_declare(exchange='pubsub', exchange_type=ExchangeType.fanout)


queue = channel.queue_declare(queue='', exclusive=True) # let server choose random queue name, exclusive=True means server can delete queue afterwards
channel.queue_bind(exchange='pubsub', queue=queue.method.queue) # need to bind the queue to the exchange

# Consume message
channel.basic_consume(queue=queue.method.queue, auto_ack=True, on_message_callback=on_message_received)

print("Starting Consuming")
channel.start_consuming()