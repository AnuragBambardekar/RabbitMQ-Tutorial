import pika

connection_parameters = pika.ConnectionParameters('localhost')

# create a connection
connection = pika.BlockingConnection(connection_parameters)

# create a default channel
channel = connection.channel()

# declare a queue
channel.queue_declare(queue='letterbox')

# publish message to queue via default exchange
message = 'hello world'

# send it
channel.basic_publish(exchange='', routing_key='letterbox', body=message)

print(f"Sent message: {message}")

# close the connection
connection.close()
