from dateutil.parser import isoparse
import requests
import datetime
import config
from json import dumps
from kafka import KafkaProducer
from time import sleep
from prometheus_client.core import GaugeMetricFamily, REGISTRY, CounterMetricFamily
from prometheus_client import start_http_server


# producer = KafkaProducer(
#         bootstrap_servers=['kafka:9093'],
#         value_serializer=lambda x: dumps(x).encode('utf-8')
#     )
#
# class CollectProducterMetrics(object):
#     def __init__(self):
#         pass
#
#     def collect(self):
#         metrics = producer.metrics()
#
#         producer_response_rate = GaugeMetricFamily("producer_response_rate", "Producer Response Rate", labels=["producer_response_rate"])
#         producer_response_rate.add_metric(['producer_response_rate'],  metrics['producer-metrics']['response-rate'])
#         yield producer_response_rate
#
#         producer_request_rate = GaugeMetricFamily("producer_request_rate", "Producer Request Rate", labels=["producer_request_rate"])
#         producer_request_rate.add_metric(['producer_request_rate'], metrics['producer-metrics']['request-rate'])
#         yield producer_request_rate
#
#         producer_request_latency_avg = GaugeMetricFamily("producer_request_latency_avg", "Producer Request Latency Avg", labels=["producer_request_latency_avg"])
#         producer_request_latency_avg.add_metric(['producer_request_latency_avg'], metrics['producer-metrics']['request-latency-avg'])
#         yield producer_request_latency_avg
#
#         producer_outgoing_byte_rate = GaugeMetricFamily("producer_outgoing_byte_rate", "Producer Outgoing Byte Rate", labels=["producer_outgoing_byte_rate"])
#         producer_outgoing_byte_rate.add_metric(['producer_outgoing_byte_rate'], metrics['producer-metrics']['outgoing-byte-rate'])
#         yield producer_outgoing_byte_rate
#
# def append_last_msgs(results, last_timestamp):
#
#     # YouTube API Configurations:
#
#     LIVECHATID = config.LIVECHATID
#     API_KEY = config.YOUR_API_KEY
#     pollid = config.pollid
#
#     # Get channelID here:
#     # https://developers.google.com/youtube/v3/live/docs/liveBroadcasts/list
#     channelId = "UC9EOQimDbyYjbyutqeltXJg"
#
#     # https://youtube.googleapis.com/youtube/v3/liveChat/messages?key=[YOUR_API_KEY]
#     baseurl = f"https://youtube.googleapis.com/youtube/v3/liveChat/messages?liveChatId={LIVECHATID}&part=snippet&key={API_KEY}"
#
#     # Setting initial timestamp:
#
#     if not last_timestamp:
#         last_timestamp = datetime.datetime.utcnow()
#         last_timestamp = last_timestamp.replace(tzinfo=datetime.timezone.utc)
#         print("Starting timestamp", last_timestamp)
#     timestamps = [last_timestamp]
#
#     # Hit the base url and exit the program if the status is not OK:
#
#     resp = requests.get(baseurl)
#     if not resp.status_code == 200:
#         print(resp)
#         exit
#
#     # Extract messages from the response:
#
#     msgs = resp.json()
#
#     for msg in msgs["items"]:
#         timestamp = isoparse(msg['snippet']['publishedAt'])
#
#         # If it is a new message:
#
#         if timestamp > last_timestamp:
#
#             timestamps.append(timestamp)
#             if msg['kind'] == 'youtube#liveChatMessage':
#                 msg_text = msg['snippet']['displayMessage']
#                 print("Message Here:")
#                 print(msg_text)
#
#                 # Publish the message data to the Kafka topic - ytchats:
#
#                 data = msg_text
#                 producer.send('ytchats', value=data)
#
#     return results, max(timestamps)
#
#
# start_http_server(9000)
# REGISTRY.register(CollectProducterMetrics())
#
# results = {}
# last_timestamp = None
# while True:
#     results, last_timestamp = append_last_msgs(results, last_timestamp)


producer = KafkaProducer(
        bootstrap_servers=['kafka:9093'],
        value_serializer=lambda x: dumps(x).encode('utf-8')
    )


class CollectProducterMetrics(object):
    def __init__(self):
        pass

    def collect(self):
        metrics = producer.metrics()

        producer_response_rate = GaugeMetricFamily("producer_response_rate", "Producer Response Rate", labels=["producer_response_rate"])
        producer_response_rate.add_metric(['producer_response_rate'],  metrics['producer-metrics']['response-rate'])
        yield producer_response_rate

        producer_request_rate = GaugeMetricFamily("producer_request_rate", "Producer Request Rate", labels=["producer_request_rate"])
        producer_request_rate.add_metric(['producer_request_rate'], metrics['producer-metrics']['request-rate'])
        yield producer_request_rate

        producer_request_latency_avg = GaugeMetricFamily("producer_request_latency_avg", "Producer Request Latency Avg", labels=["producer_request_latency_avg"])
        producer_request_latency_avg.add_metric(['producer_request_latency_avg'], metrics['producer-metrics']['request-latency-avg'])
        yield producer_request_latency_avg

        producer_outgoing_byte_rate = GaugeMetricFamily("producer_outgoing_byte_rate", "Producer Outgoing Byte Rate", labels=["producer_outgoing_byte_rate"])
        producer_outgoing_byte_rate.add_metric(['producer_outgoing_byte_rate'], metrics['producer-metrics']['outgoing-byte-rate'])
        yield producer_outgoing_byte_rate

start_http_server(9000)
REGISTRY.register(CollectProducterMetrics())

while True:

    # print("Iteration", j)
    print("IT'S ON")
    data = 'amazing stream'
    producer.send('ytchats', value=data)
    metrics = producer.metrics()
    print("printing producer metrics")
    print(type(metrics))
    print(metrics['producer-metrics']['response-rate'])

    sleep(2)