import pika
from pika.exchange_type import ExchangeType

connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

# Declare two exchanges
channel.exchange_declare('simpleHashing', "x-consistent-hash")

# routingKey = "Hash Me!"
routingKey = "766a789ydhsh me 31fdaskjnofa7 ][]"
message = "Core Message"

channel.basic_publish(exchange='simpleHashing', 
                      routing_key=routingKey, 
                      body=message)

print(f"Sent Message: {message}")
connection.close()