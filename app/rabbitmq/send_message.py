import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='localhost', 
        credentials=pika.PlainCredentials(
            username='userPhen', 
            password='Fantasy24'
        )
    )
)
channel = connection.channel()
channel.queue_declare(queue='hello')

channel.basic_publish(
    exchange='',
    routing_key='hello',
    body='Hello there'
)
print('Send message')
connection.close()
