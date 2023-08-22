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
channel.exchange_declare(exchange='headersExchange', exchange_type=ExchangeType.headers)

# declare a queue
channel.queue_declare(queue='letterbox')

# binding arguments
bind_args = {
    'x-match':'all', # expecting both name and age
    'name':'Bamba',
    'age':'24'
}
# 'x-match':'any', # expecting any of name or age

# bind the queue
channel.queue_bind('letterbox', 'headersExchange', arguments=bind_args)

channel.basic_consume(queue='letterbox', auto_ack=True, on_message_callback=on_message_received)

print("Started consuming messages...")
channel.start_consuming()



