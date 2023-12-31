import pika
import uuid

def on_reply_message_received(ch, method, properties, body):
    print(f"Reply received: {body}")

connection_params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_params)

channel = connection.channel()

# Declare a reply queue
reply_queue = channel.queue_declare(queue='', exclusive=True)
# Set up a consumer on the reply queue
channel.basic_consume(queue=reply_queue.method.queue, auto_ack=True, on_message_callback=on_reply_message_received)

# request queue was created on server-side script
# channel.queue_declare(queue='request-queue')

message = "Can I request a reply?"
corr_id = str(uuid.uuid4())

print(f"Sending Request: {corr_id}")
# Publish the request message
channel.basic_publish(exchange='', routing_key='request-queue', 
                      properties= pika.BasicProperties(
                          reply_to=reply_queue.method.queue,
                          correlation_id=corr_id
                      ),
                      body=message)

print("Starting Client")

channel.start_consuming()