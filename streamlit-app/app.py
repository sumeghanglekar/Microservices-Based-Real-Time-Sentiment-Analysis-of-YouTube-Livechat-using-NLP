import streamlit as st  # web development
import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import time  # to simulate a real time data, time loop
import plotly.express as px  # interactive charts
from kafka import KafkaConsumer
from json import loads
from time import sleep

consumer = KafkaConsumer(
    'ytchats',
    bootstrap_servers=['kafka:9093'],
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='my-group-id',
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)

# read csv from a github repo
df = pd.read_csv("https://raw.githubusercontent.com/Lexie88rus/bank-marketing-analysis/master/bank.csv")

st.set_page_config(
    page_title='Real-Time Data Science Dashboard',
    page_icon='✅',
    layout='wide'
)

# dashboard title

st.title("Real-Time / Live Data Science Dashboard")

# top-level filters 

job_filter = st.selectbox("Select the Job", pd.unique(df['job']))

# creating a single-element container.
placeholder = st.empty()

# dataframe filter 

df = df[df['job'] == job_filter]

# near real-time / live feed simulation 

while True:
    # while True:
    data = []
    df['age_new'] = df['age'] * np.random.choice(range(1, 5))
    df['balance_new'] = df['balance'] * np.random.choice(range(1, 5))

    newdf = pd.DataFrame(data, columns=['Numbers'])

    for event in consumer:
        event_data = event.value
        data.append(event_data)
        print(data)
        # Do whatever you want
        # print(event_data)
        sleep(2)
    # creating KPIs 
    avg_age = np.mean(df['age_new'])

    count_married = int(df[(df["marital"] == 'married')]['marital'].count() + np.random.choice(range(1, 30)))

    balance = np.mean(df['balance_new'])

    with placeholder.container():
        # create three columns
        kpi1, kpi2, kpi3 = st.columns(3)

        # fill in those three columns with respective metrics or KPIs 
        kpi1.metric(label="Age ⏳", value=round(avg_age), delta=round(avg_age) - 10)
        kpi2.metric(label="Married Count 💍", value=int(count_married), delta=- 10 + count_married)
        kpi3.metric(label="A/C Balance ＄", value=f"$ {round(balance, 2)} ",
                    delta=- round(balance / count_married) * 100)

        # create two columns for charts 

        fig_col1, fig_col2 = st.columns(2)
        with fig_col1:
            st.markdown("### First Chart")
            fig = px.density_heatmap(data_frame=df, y='age_new', x='marital')
            st.write(fig)
        with fig_col2:
            st.markdown("### Second Chart")
            fig2 = px.histogram(data_frame=df, x='age_new')
            st.write(fig2)
        st.markdown("### Detailed Data View")
        st.dataframe(newdf)
        time.sleep(1)
    # placeholder.empty()