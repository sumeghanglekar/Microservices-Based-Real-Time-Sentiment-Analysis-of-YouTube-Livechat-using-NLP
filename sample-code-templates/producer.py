from time import sleep
from json import dumps
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],   #server that the producer contacts
    value_serializer=lambda x: dumps(x).encode('utf-8') #returns deserialized message value
)   

for j in range(9999):
    print("Iteration", j)
    data = {'counter': j}
    producer.send('topic_test', value=data)
    sleep(1)