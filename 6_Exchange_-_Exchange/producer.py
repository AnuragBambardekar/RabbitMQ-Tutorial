import pika
from pika.exchange_type import ExchangeType

connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

# Declare two exchanges
channel.exchange_declare(exchange='firstExchange', exchange_type=ExchangeType.direct)
channel.exchange_declare(exchange='secondExchange', exchange_type=ExchangeType.fanout)

# Bind the two exchanges
channel.exchange_bind("secondExchange","firstExchange")

message = "hello this message has gone through multiple exchanges"

channel.basic_publish(exchange='firstExchange', routing_key='', body=message)

print(f"Sent Message: {message}")
connection.close()

"""
send message to first exchange
first exchange will send that message to second exchange which is a fanout
the fanout exchange will push that to the consumer

"""