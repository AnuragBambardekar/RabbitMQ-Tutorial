import pika
from pika.exchange_type import ExchangeType

connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

# enables publish confirm
channel.confirm_delivery()

# enables transactions
# channel.tx_select()

channel.exchange_declare(exchange='pubsub', exchange_type=ExchangeType.fanout)

# create a durable queue that survives restarts
channel.queue_declare("test", durable=True)

message = "Hello I want to broadcast this message."

channel.basic_publish(
    exchange='pubsub',
    routing_key='',
    properties=pika.BasicProperties(
        headers={'name':'bamba'},
        delivery_mode=1,
        expiration='13434343',
        content_type="application/json"
    ), 
    body=message,
    mandatory=True # publishing is mandatory i.e. receive a notification of failure
)

# commit a transaction
# channel.tx_commit()

# rollback a transaction
# channel.tx_rollback()

print(f"Sent Message: {message}")

connection.close()