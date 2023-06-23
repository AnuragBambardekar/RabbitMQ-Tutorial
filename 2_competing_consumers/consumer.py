import pika
import time
import random

def on_message_received(ch, method, properties, body):
    processing_time = random.randint(1,5)
    print(f"Received new message: {body}, will take {processing_time} seconds to process")
    time.sleep(processing_time)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print("Finished processing the message.")

connection_parameters = pika.ConnectionParameters('localhost')

# create a connection
connection = pika.BlockingConnection(connection_parameters)

# create a default channel
channel = connection.channel()

# declare a queue
channel.queue_declare(queue='letterbox')

# set prefetch count
channel.basic_qos(prefetch_count=1) # Can take this line out for having the default round-robin fashion

channel.basic_consume(queue='letterbox', on_message_callback=on_message_received)

print("Started consuming messages...")
channel.start_consuming()
