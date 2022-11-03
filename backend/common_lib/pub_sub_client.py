import pika, json

class PubSubClient:
    def __init__(self, host) -> None: 
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host)
        )
        self.channel = self.connection.channel()
    
    def setup(self, exchange, exchange_type, queue_name, ) -> None:
        self.channel.queue_declare(queue=queue_name)
        self.channel.exchange_declare(exchange=exchange, exchange_type=exchange_type)

    def run(self):
        pass

    def close(self):
        pass

class Subscriber(PubSubClient):
    exchange = ''
    exchange_type = ''
    queue_name = ''
    routing_key = ''
    host=''

    def on_message_callback(self, ch, method, properties, body) -> None:
        message = json.loads(body)
        print(f'Recieved {message}')

    
    def setup(self, exchange, exchange_type, queue_name, routing_key, prefetch_count=10) -> None:
        super().setup(exchange, exchange_type, queue_name)

        self.channel.queue_bind(queue=queue_name, exchange=exchange, routing_key=routing_key)
        self.channel.basic_qos(prefetch_count=prefetch_count)
        self.channel.basic_consume(queue=queue_name, on_message_callback=self.on_message_callback, auto_ack=True)
    
    def run(self):
        print('Waiting for message. To exit press Ctrl+C')
        self.channel.start_consuming()

class Publisher(PubSubClient):
    def __init__(self, host):
        PubSubClient.__init__(self, host)
        
    def run(self, exchange, routing_key, message):
        body = bytes(json.dumps(message), encoding='utf-8')
        self.channel.basic_publish(exchange=exchange, 
                                routing_key=routing_key, body=body)



