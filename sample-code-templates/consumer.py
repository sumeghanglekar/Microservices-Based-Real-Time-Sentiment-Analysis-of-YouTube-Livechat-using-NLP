from kafka import KafkaConsumer
from json import loads
from time import sleep

consumer = KafkaConsumer(
    'ytchats',  #topic
    bootstrap_servers=['localhost:9092'],   #server that the consumer contacts
    auto_offset_reset='latest', #resets the offset to the most recent message
    enable_auto_commit=True,    #offset will periodically commit in the background
    group_id='my-group-id',     #consumer group for fetching and commiting offsets
    value_deserializer=lambda x: loads(x.decode('utf-8'))   #returns deserialized message value
)
for event in consumer:
    event_data = event.value
    # Do whatever you want
    print(event_data)
    sleep(0.5)