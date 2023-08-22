import pika
import uuid
from pika.exchange_type import ExchangeType

def on_request_message_received(ch, method, properties, body):
    print(f"Request received: {properties.correlation_id}")
    ch.basic_publish('', routing_key=properties.reply_to, body=f"Hey its your reply to: {properties.correlation_id}")

connection_params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_params)

channel = connection.channel()

# Declare a request queue
reply_queue = channel.queue_declare(queue='request-queue', exclusive=True)
# Set up a consumer on the request queue
# server invokes the on_request_message_received callback, which includes the request message and its properties.
channel.basic_consume(queue="request-queue", auto_ack=True, on_message_callback=on_request_message_received)


print("Starting Server")

channel.start_consuming()