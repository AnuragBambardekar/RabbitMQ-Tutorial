import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

queue_name = 'my_queue'
channel.queue_declare(queue=queue_name)

# Consume messages
for method_frame, properties, body in channel.consume(queue_name, auto_ack=False):
    # Unpack the delivery tag from the method frame
    delivery_tag = method_frame.delivery_tag
    
    # Process the message here
    print(f"Received message: {body}")

    # Acknowledge the message using the delivery tag
    channel.basic_ack(delivery_tag=delivery_tag)

# Close the connection
connection.close()
