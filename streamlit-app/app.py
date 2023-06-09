import streamlit as st  # web development
import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import time  # to simulate a real time data, time loop
import plotly.express as px  # interactive charts
from kafka import KafkaConsumer
from json import loads
from time import sleep
import requests
import json
from prometheus_client.core import GaugeMetricFamily, REGISTRY, CounterMetricFamily
from prometheus_client import start_http_server

consumer = KafkaConsumer(
    'ytchats',
    bootstrap_servers=['kafka:9093'],
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='my-group-id',
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)

class CollectConsumerMetrics(object):
    def __init__(self):
        pass

    def collect(self):
        metrics = consumer.metrics()

        consumer_response_rate = GaugeMetricFamily("consumer_response_rate", "Consumer Response Rate", labels=["consumer_response_rate"])
        consumer_response_rate.add_metric(['consumer_response_rate'],  metrics['consumer-metrics']['response-rate'])
        yield consumer_response_rate

        consumer_request_rate = GaugeMetricFamily("consumer_request_rate", "Consumer Request Rate", labels=["consumer_request_rate"])
        consumer_request_rate.add_metric(['consumer_request_rate'], metrics['consumer-metrics']['request-rate'])
        yield consumer_request_rate

        consumer_request_latency_avg = GaugeMetricFamily("consumer_request_latency_avg", "Consumer Request Latency Avg", labels=["consumer_request_latency_avg"])
        consumer_request_latency_avg.add_metric(['consumer_request_latency_avg'], metrics['consumer-metrics']['request-latency-avg'])
        yield consumer_request_latency_avg

        consumer_outgoing_byte_rate = GaugeMetricFamily("consumer_outgoing_byte_rate", "Consumer Outgoing Byte Rate", labels=["consumer_outgoing_byte_rate"])
        consumer_outgoing_byte_rate.add_metric(['consumer_outgoing_byte_rate'], metrics['consumer-metrics']['outgoing-byte-rate'])
        yield consumer_outgoing_byte_rate

        consumer_fetch_rate = GaugeMetricFamily("consumer_fetch_rate", "Consumer Fetch Rate",labels=["consumer_fetch_rate"])
        consumer_fetch_rate.add_metric(['consumer_fetch_rate'], metrics['consumer-fetch-manager-metrics']['fetch-rate'])
        yield consumer_fetch_rate

        consumer_records_lag_max = GaugeMetricFamily("consumer_records_lag_max", "Consumer Records Lag Max", labels=["consumer_records_lag_max"])
        consumer_records_lag_max.add_metric(['consumer_records_lag_max'], metrics['consumer-fetch-manager-metrics']['records-lag-max'])
        yield consumer_records_lag_max

start_http_server(9006)
REGISTRY.register(CollectConsumerMetrics())

url = "http://172.22.0.7:5000/fastSentiment"

st.set_page_config(
    page_title='Real-Time Sentiment Analysis of Youtube LiveChat',
    page_icon='✅',
    layout='wide'
)

# dashboard title

st.title("Real-Time Sentiment Analysis of Youtube LiveChat")

# creating a single-element container.
placeholder = st.empty()

while True:
    data = []
    total_messages = 0
    positive_messages = 0
    negative_messages = 0
    sentiment = 0
    counts = {'positive_messages':positive_messages,
              'negative_messages': negative_messages}
    df = pd.DataFrame(counts,index=[0])
    line_data = {"sentiment": sentiment}
    line_data_df = pd.DataFrame(line_data,index=[0])

    for event in consumer:
        print(df)
        event_data = event.value
        data.append(event_data)
        print(data)

        payload = json.dumps({
            "msg": event_data
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)

        if response.text == 'positive':
            df['positive_messages'] = df['positive_messages'] + 1
            total_messages = total_messages + 1
            sentiment = sentiment + 1
        elif response.text == 'negative':
            df['negative_messages'] = df['negative_messages'] + 1
            total_messages = total_messages + 1
            sentiment = sentiment - 1
        else:
            total_messages = total_messages + 1
            continue

        metrics = consumer.metrics()
        print("printing metrics")
        print(type(metrics))
        print(metrics['consumer-fetch-manager-metrics']['records-lag-max'])


        with placeholder.container():
            kpi1, kpi2, kpi3 = st.columns(3)

            # fill in those three columns with respective metrics or KPIs
            kpi1.metric(label="Total Messages", value=total_messages)
            kpi2.metric(label="Positive Messages", value=df['positive_messages'])
            kpi3.metric(label="Negative Messages", value=df['negative_messages'])

            # create two columns for charts

            fig_col1, fig_col2 = st.columns(2)
            with fig_col1:
                st.markdown("Sentiment Distribution of Messages")
                st.bar_chart(df)

            with fig_col2:
                st.markdown("Sentiment Over Time")
                line_data_df.loc[len(line_data_df.index)] = [sentiment]
                print(line_data_df)
                st.line_chart(line_data_df)

            fig_col3, fig_col4 = st.columns(2)
            with fig_col3:
                st.markdown("Tabular View")
                st.dataframe(df)
