import pika
from pika.exchange_type import ExchangeType

def on_message_received(ch, method, properties, body):
    print(f"Analytics Service: Received new message: {body}")

connection_params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_params)

channel = connection.channel()

# direct exchange
# channel.exchange_declare(exchange='routing', exchange_type=ExchangeType.direct)

# topic exchange
channel.exchange_declare(exchange='mytopicexchange', exchange_type=ExchangeType.topic)

queue = channel.queue_declare(queue='', exclusive=True) # let server choose random queue name, exclusive=True means server can delete queue on connection close

# direct exchange binding
# channel.queue_bind(exchange='routing', queue=queue.method.queue, routing_key='analyticsonly') # need to bind the queue to the exchange
# channel.queue_bind(exchange='routing', queue=queue.method.queue, routing_key='both') # need to bind the queue to the exchange

# topic exchange
channel.queue_bind(exchange='mytopicexchange', queue=queue.method.queue, routing_key='*.europe.*')

# Consume message
channel.basic_consume(queue=queue.method.queue, auto_ack=True, on_message_callback=on_message_received)

print("Starting Consuming")
channel.start_consuming()