from dateutil.parser import isoparse
import requests
import datetime
import config
from json import dumps
from kafka import KafkaProducer
from time import sleep
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway



# def append_last_msgs(results, last_timestamp):
    
#     # YouTube API Configurations:

#     LIVECHATID = config.LIVECHATID
#     API_KEY = config.YOUR_API_KEY
#     pollid = config.pollid

#     # Get channelID here:
#     # https://developers.google.com/youtube/v3/live/docs/liveBroadcasts/list
#     channelId = "UC9EOQimDbyYjbyutqeltXJg"

#     # https://youtube.googleapis.com/youtube/v3/liveChat/messages?key=[YOUR_API_KEY]
#     baseurl = f"https://youtube.googleapis.com/youtube/v3/liveChat/messages?liveChatId={LIVECHATID}&part=snippet&key={API_KEY}"


#     #Kafka Producer:

#     producer = KafkaProducer(
#         bootstrap_servers=['kafka:9093'],
#         value_serializer=lambda x: dumps(x).encode('utf-8')
#     )

#     # Setting initial timestamp:

#     if not last_timestamp:
#         last_timestamp = datetime.datetime.utcnow()
#         last_timestamp = last_timestamp.replace(tzinfo=datetime.timezone.utc)
#         print("Starting timestamp", last_timestamp)
#     timestamps = [last_timestamp]

#     # Hit the base url and exit the program if the status is not OK:

#     resp = requests.get(baseurl)
#     if not resp.status_code == 200:
#         print(resp)
#         exit

#     # Extract messages from the response:

#     msgs = resp.json()

#     for msg in msgs["items"]:
#         timestamp = isoparse(msg['snippet']['publishedAt'])

#         # If it is a new message:

#         if timestamp > last_timestamp:

#             timestamps.append(timestamp)
#             if msg['kind'] == 'youtube#liveChatMessage':
#                 msg_text = msg['snippet']['displayMessage']
#                 print("Message Here:")
#                 print(msg_text)

#                 # Publish the message data to the Kafka topic - ytchats:

#                 data = msg_text
#                 producer.send('ytchats', value=data)

#     return results, max(timestamps)

# results = {}
# last_timestamp = None
# while True:
#     results, last_timestamp = append_last_msgs(results, last_timestamp)


producer = KafkaProducer(
        bootstrap_servers=['kafka:9093'],
        value_serializer=lambda x: dumps(x).encode('utf-8')
    )


while True:
    # print("Iteration", j)
    print("IT'S ON")
    data = 'amazing stream'
    producer.send('ytchats', value=data)
    metrics = producer.metrics()
    print("printing metrics")
    print(type(metrics))
    print(metrics)

    registry = CollectorRegistry()
    g = Gauge('job_last_success_unixtime', 'Last time a batch job successfully finished', registry=registry)
    g.set_to_current_time()
    push_to_gateway('http://172.22.0.4:9090', job='batchA', registry=registry)


    sleep(2)