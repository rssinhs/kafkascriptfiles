from kafka import KafkaProducer
a=1234567
producer = KafkaProducer(bootstrap_servers='localhost:9092')
producer.send('TestTopic', b'Hello, World!')
#producer.send('TestTopic',a)
#producer.send('TestTopic', key=b'message-two', value=b'This is Kafka-Python')
producer.flush()