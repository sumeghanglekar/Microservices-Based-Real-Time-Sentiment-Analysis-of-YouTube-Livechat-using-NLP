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

consumer = KafkaConsumer(
    'ytchats',
    bootstrap_servers=['kafka:9093'],
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='my-group-id',
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)

url = "http://172.22.0.6:5000/fastSentiment"

# read csv from a github repo
# df = pd.read_csv("https://raw.githubusercontent.com/Lexie88rus/bank-marketing-analysis/master/bank.csv")

st.set_page_config(
    page_title='Real-Time Data Science Dashboard',
    page_icon='✅',
    layout='wide'
)

# dashboard title

st.title("Real-Time Sentiment Analysis of Youtube LiveChat")

# creating a single-element container.
placeholder = st.empty()

# dataframe filter 

# df = df[df['job'] == job_filter]

# near real-time / live feed simulation 

while True:
    # while True:
    data = []
    total_messages = 0
    positive_messages = 0
    negative_messages = 0
    counts = {'total_messages':total_messages,
              'positive_messages':positive_messages,
              'negative_messages': negative_messages}
    df = pd.DataFrame(counts,index=[0])

    newdf = pd.DataFrame(data, columns=['Numbers'])

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
        elif response.text == 'negative':
            df['negative_messages'] = df['negative_messages'] + 1
        else:
            continue


        # creating KPIs
        # avg_age = np.mean(df['age_new'])

        # count_married = int(df[(df["marital"] == 'married')]['marital'].count() + np.random.choice(range(1, 30)))

        # balance = np.mean(df['balance_new'])

        with placeholder.container():
            # create three columns
            kpi1, kpi2, kpi3 = st.columns(3)

            # fill in those three columns with respective metrics or KPIs
            kpi1.metric(label="Total Messages", value=df['total_messages'])
            kpi2.metric(label="Positive Messages", value=df['positive_messages'])
            kpi3.metric(label="Negative Messages", value=df['negative_messages'])

            # create two columns for charts

            fig_col1, fig_col2 = st.columns(2)
            with fig_col1:
                st.bar_chart(df)
            # with fig_col2:
            #     st.markdown("### Second Chart")
            #     fig2 = px.histogram(data_frame=df, x='age_new')
            #     st.write(fig2)
            # st.markdown("### Detailed Data View")
            st.dataframe(df)
    # placeholder.empty()