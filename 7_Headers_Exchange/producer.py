import pika
from pika.exchange_type import ExchangeType

connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

# Declare two exchanges
channel.exchange_declare(exchange='headersExchange', exchange_type=ExchangeType.headers)

message = "hello this message will be sent with headers"

channel.basic_publish(exchange='headersExchange', 
                      routing_key='', 
                      body=message,
                      properties=pika.BasicProperties(headers={'name':'Bamba'}))

print(f"Sent Message: {message}")
connection.close()