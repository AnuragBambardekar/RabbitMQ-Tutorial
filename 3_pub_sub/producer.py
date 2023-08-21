import pika
from pika.exchange_type import ExchangeType

connection_params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_params)

channel = connection.channel()

# no need to declare queue now because publisher need not know about queues, because each consumer will have it's own dedicated queue
# channel.queue_declare(queue='letterbox')

# Declare Fanout Exchange
channel.exchange_declare(exchange='pubsub', exchange_type=ExchangeType.fanout)

message = "Hello I want to broadcast this message"

# send it to 'pubsub' exchange
channel.basic_publish(exchange='pubsub', routing_key='', body=message)

print(f"Sent Message: {message}")

connection.close()