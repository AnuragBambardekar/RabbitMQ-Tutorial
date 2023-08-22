import pika

# Establish a connection to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare the queue
queue_name = 'my_queue'
channel.queue_declare(queue=queue_name)

# Define a list of messages to send
messages_to_send = [
    "Message 1",
    "Message 2",
    "Message 3",
]

# Publish each message to the queue
for message in messages_to_send:
    channel.basic_publish(exchange='',
                          routing_key=queue_name,
                          body=message)
    print(f"Sent: {message}")

# Close the connection
connection.close()
