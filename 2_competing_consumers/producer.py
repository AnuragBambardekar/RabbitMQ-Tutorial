import pika
import time
import random

connection_parameters = pika.ConnectionParameters('localhost')

# create a connection
connection = pika.BlockingConnection(connection_parameters)

# create a default channel
channel = connection.channel()

# declare a queue
channel.queue_declare(queue='letterbox')

# add id to message
messageId = 1

# send it
while True:
    # publish message to queue via default exchange
    message = f'Sending Message ID: {messageId}'

    channel.basic_publish(exchange='', routing_key='letterbox', body=message)

    print(f"Sent message: {message}")

    time.sleep(random.randint(1,4))

    messageId += 1
