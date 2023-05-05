# Microservices Based Real-Time Sentiment Analysis of YouTube Live Chat using NLP
A microservices-based application that studies the sentiment of YouTube live chat comments in real-time using Python, YouTube API, Docker, Kafka, Prometheus and Grafana.
The system uses YouTube Data API to fetch live chats from the livestream. 

### Requirements & Prerequisites:
1. Need docker installed on system
2. Download the model_tweet.bin [file](https://drive.google.com/file/d/1X6OaERlUnJNXjz26CNOnP6XcOXZPNqV9/view?usp=sharing) and place it the sentiment-analyzer directory (you can train your own model and use it)
3. The system is designed to pull YouTube live stream chats. You need to update the config.py file with API KEY and LIVE CHAT ID.
   1. The YouTube Data API needs to be enabled at this [link](https://console.cloud.google.com/apis/api/youtube.googleapis.com/)
   2. The API KEY can be generated at this [link](https://console.cloud.google.com/apis/credentials)  
   3. The LIVE CHAT ID can be obtained by running the API on this [link](https://developers.google.com/youtube/v3/live/docs/liveBroadcasts/list?apix=true#try-it) using the google account running the live stream. 
      #### Note: The live stream must be on before fetching the LIVE CHAT ID
   
###### In case you don't have a live stream and want to test the system, you can change the DockerFile in get-yt-chats directory to run the simulateProducer.py instead of consumeYtChats.py. (It is a sample file which runs Kafka Producer and randomly sends messages to Producer so as to simulate a live chat).

### Steps:
1. Run 'docker compose up' inside the kafka-docker directory
2. Run 'docker compose up' inside the sentiment-analyzer directory
3. Run 'docker compose up' inside the get-yt-chats directory
4. Run 'docker compose up' inside the streamlit-app directory
5. The frontend can be accessed at http://localhost:8002/
6. Grafana can be accessed at http://localhost:3000/
   1. You can log in using default login and password: admin & admin
   2. Check if prometheus data source is added. Click on sidebar and connections. If you don't see a prometheus data source, add a prometheus data source and enter the url as 'http://172.22.0.2:9090'.
   3. Once the data source is added navigate to sidebar and dashboards. If you don't see any dashboards you can import it using the json file provided under /grafana-dashboards/kafka-overview.json
   4. Once it's imported you can see all the kafka overview alongside producer and consumer metrics.


### Application Demo:

### Resources:
1. https://www.datadoghq.com/blog/monitoring-kafka-performance-metrics/
2. https://stackoverflow.com/questions/59924566/export-prometheus-metrics-using-python-code
3. https://streamlit.io/
4. https://developers.google.com/youtube/v3/live/getting-started
5. https://medium.com/@lope.ai/sentiment-analysis-example-using-fasttext-6b1b4d334c53
6. https://kafka-python.readthedocs.io/en/master/


