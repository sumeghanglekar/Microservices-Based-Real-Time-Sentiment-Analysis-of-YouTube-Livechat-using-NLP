from flask import Flask
from dateutil.parser import isoparse
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.ticker import MaxNLocator
import difflib
import requests
import datetime
import time
import config
from time import sleep
from json import dumps
from kafka import KafkaProducer


app = Flask(__name__)

@app.route('/')
def test():
    temp = index()
    return temp

def index():
    return 'Hello'

@app.route('/getChats')

def main():
    while True:
        results, last_timestamp = append_last_msgs(results, last_timestamp)

    return 'Success'


def append_last_msgs(results, last_timestamp):
    LIVECHATID = config.LIVECHATID
    API_KEY = config.YOUR_API_KEY
    # pollid = config.pollid
    # Get channelID here:
    # https://developers.google.com/youtube/v3/live/docs/liveBroadcasts/list
    # channelId = "UC9EOQimDbyYjbyutqeltXJg"
    # https://youtube.googleapis.com/youtube/v3/liveChat/messages?key=[YOUR_API_KEY]
    baseurl = f"https://youtube.googleapis.com/youtube/v3/liveChat/messages?liveChatId={LIVECHATID}&part=snippet&key={API_KEY}"


    #Kafka Producer
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
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



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')