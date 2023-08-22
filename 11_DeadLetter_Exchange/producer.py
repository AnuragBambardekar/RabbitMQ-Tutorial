import pika
from pika.exchange_type import ExchangeType

connection_parameters = pika.ConnectionParameters('localhost')

# create a connection
connection = pika.BlockingConnection(connection_parameters)

# create a default channel
channel = connection.channel()

# declare main exchange
channel.exchange_declare(exchange='mainexchange', exchange_type=ExchangeType.direct)

# publish message
message = 'hello world - this message will expire...'

# send it
channel.basic_publish(exchange='mainexchange', routing_key='test', body=message)

print(f"Sent message: {message}")

# close the connection
connection.close()
