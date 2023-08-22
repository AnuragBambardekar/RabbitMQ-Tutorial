import pika

# Establish a connection to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

try:
    # Enable transaction mode
    channel.tx_select()

    # Publish a message within the transaction
    channel.basic_publish(exchange='', routing_key='queue_name', body='Hello, RabbitMQ!')

    # Simulate an error or condition that would require a rollback
    # raise Exception("Something went wrong!")

    # Commit the transaction if everything is successful
    channel.tx_commit()

except Exception as e:
    # Rollback the transaction in case of an exception
    channel.tx_rollback()
    print(f"Transaction rolled back: {e}")

finally:
    # Close the channel and connection
    channel.close()
    connection.close()
