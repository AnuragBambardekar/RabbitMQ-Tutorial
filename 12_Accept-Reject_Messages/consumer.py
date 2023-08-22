import pika
from pika.exchange_type import ExchangeType

def on_message_received(ch, method, properties, body):

    if (method.delivery_tag % 5 == 0):
        ch.basic_ack(delivery_tag=method.delivery_tag, multiple=True)
        # ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False, multiple=True)
        """
        When requeue is set to True, it means that the message(s) will be placed back in the queue for reprocessing. 
        When set to False, the message(s) will be discarded or moved to a dead-letter queue, depending on your RabbitMQ configuration.
        """

    #ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)

    print(f'Received new message: {method.delivery_tag}')

connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.exchange_declare(
    exchange='acceptrejectexchange', 
    exchange_type=ExchangeType.fanout)

channel.queue_declare(queue='letterbox')
channel.queue_bind('letterbox', 'acceptrejectexchange')

channel.basic_consume(queue='letterbox', on_message_callback=on_message_received)

print('Starting Consuming')

channel.start_consuming()