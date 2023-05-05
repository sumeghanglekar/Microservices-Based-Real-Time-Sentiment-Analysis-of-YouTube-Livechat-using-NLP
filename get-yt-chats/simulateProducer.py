from dateutil.parser import isoparse
import requests
import datetime
import config
from json import dumps
from kafka import KafkaProducer
from time import sleep
from prometheus_client.core import GaugeMetricFamily, REGISTRY, CounterMetricFamily
from prometheus_client import start_http_server
import random


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
    data = ['amazing stream','boring stream']
    index = random.randint(0, 1)

    producer.send('ytchats', value=data[index])
    metrics = producer.metrics()
    print("printing producer metrics")
    print(type(metrics))
    print(metrics['producer-metrics']['response-rate'])

    sleepduration = random.randint(0, 10)
    sleep(sleepduration)