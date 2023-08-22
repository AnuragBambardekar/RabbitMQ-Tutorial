import pika
from pika.exchange_type import ExchangeType

connection_parameters = pika.ConnectionParameters('localhost')

# create a connection
connection = pika.BlockingConnection(connection_parameters)

# create a default channel
channel = connection.channel()

# declare alt exchange and main exchange
channel.exchange_declare(exchange='altexchange', exchange_type=ExchangeType.fanout)
channel.exchange_declare(exchange='mainexchange', exchange_type=ExchangeType.direct,
                         arguments={'alternate-exchange':'altexchange'})

# publish message to queue via default exchange
message = 'hello world'

# send it
channel.basic_publish(exchange='mainexchange', routing_key='', body=message) # if we bind a different routing key, message will be sent to alt exchange

print(f"Sent message: {message}")

# close the connection
connection.close()
