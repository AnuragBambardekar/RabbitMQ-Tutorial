import pika
from pika.exchange_type import ExchangeType

def on_message1_received(ch, method, properties, body):
    print(f"Queue1 Received new message: {body}")

def on_message2_received(ch, method, properties, body):
    print(f"Queue2 Received new message: {body}")

connection_parameters = pika.ConnectionParameters('localhost')

# create a connection
connection = pika.BlockingConnection(connection_parameters)

# create a default channel
channel = connection.channel()

# declare the exchange
channel.exchange_declare('simpleHashing', "x-consistent-hash")

# declare a queue
channel.queue_declare(queue='letterbox1')
# bind the queue
channel.queue_bind('letterbox1', 'simpleHashing', routing_key='1')
channel.basic_consume(queue='letterbox1', auto_ack=True, on_message_callback=on_message1_received)

# declare a queue
channel.queue_declare(queue='letterbox2')
# bind the queue
channel.queue_bind('letterbox2', 'simpleHashing', routing_key='4') # expect this queue to get more messages
channel.basic_consume(queue='letterbox2', auto_ack=True, on_message_callback=on_message2_received)

print("Started consuming messages...")
channel.start_consuming()



