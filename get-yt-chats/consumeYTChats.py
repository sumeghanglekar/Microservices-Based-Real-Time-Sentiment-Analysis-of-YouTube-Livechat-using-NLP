from dateutil.parser import isoparse
import requests
import datetime
import config
from json import dumps
from kafka import KafkaProducer



def append_last_msgs(results, last_timestamp):
    LIVECHATID = config.LIVECHATID
    API_KEY = config.YOUR_API_KEY
    pollid = config.pollid
    # Get channelID here:
    # https://developers.google.com/youtube/v3/live/docs/liveBroadcasts/list
    channelId = "UC9EOQimDbyYjbyutqeltXJg"
    # https://youtube.googleapis.com/youtube/v3/liveChat/messages?key=[YOUR_API_KEY]
    baseurl = f"https://youtube.googleapis.com/youtube/v3/liveChat/messages?liveChatId={LIVECHATID}&part=snippet&key={API_KEY}"


    #Kafka Producer
    producer = KafkaProducer(
        bootstrap_servers=['kafka:9093'],
        value_serializer=lambda x: dumps(x).encode('utf-8')
    )

    if not last_timestamp:
        last_timestamp = datetime.datetime.utcnow()
        last_timestamp = last_timestamp.replace(tzinfo=datetime.timezone.utc)
        print("Starting timestamp", last_timestamp)
    timestamps = [last_timestamp]

    resp = requests.get(baseurl)
    if not resp.status_code == 200:
        print(resp)
        exit
    msgs = resp.json()

    for msg in msgs["items"]:
        timestamp = isoparse(msg['snippet']['publishedAt'])
        if timestamp > last_timestamp:

            timestamps.append(timestamp)
            if msg['kind'] == 'youtube#liveChatMessage':
                msg_text = msg['snippet']['displayMessage']
                print("Message Here:")
                print(msg_text)

                data = msg_text
                producer.send('ytchats', value=data)

    return results, max(timestamps)

results = {}
last_timestamp = None
while True:
    results, last_timestamp = append_last_msgs(results, last_timestamp)