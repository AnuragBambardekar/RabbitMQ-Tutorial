import pika
from pika.exchange_type import ExchangeType

connection_params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_params)

channel = connection.channel()

# no need to declare queue now because publisher need not know about queues, because each consumer will have it's own dedicated queue
# channel.queue_declare(queue='letterbox')

# Declare direct Exchange
# channel.exchange_declare(exchange='routing', exchange_type=ExchangeType.direct)

# Declare topic Exchange
channel.exchange_declare(exchange='mytopicexchange', exchange_type=ExchangeType.topic)


# Publish direct Exchange
# message = "This message needs to be routed."
# channel.basic_publish(exchange='routing', routing_key='both', body=message) # could also send just routing_key=analyticsonly
# print(f"Sent Message: {message}")

# Publish topic Exchange
user_payments_message = 'A european user paid for something'
channel.basic_publish(exchange='mytopicexchange', routing_key='user.europe.payments', body=user_payments_message)
print(f"Sent Message: {user_payments_message}")

business_order_message = 'A european business ordered goods'
channel.basic_publish(exchange='mytopicexchange', routing_key='business.europe.orders', body=business_order_message)
print(f"Sent Message: {business_order_message}")




connection.close()