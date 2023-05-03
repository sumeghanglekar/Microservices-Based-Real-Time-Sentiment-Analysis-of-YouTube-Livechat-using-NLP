# Real-time-Sentiment-Analysis-of-YouTube-live-chat-using-NLP-and-Microservices
A microservices-based application that studies the sentiment of YouTube live chat comments in real-time using Python, YouTube API, Docker containers and Kafka streaming service.

Steps:
1. Run "docker compose up" inside the kafka-docker directory

2. Check if Prometheus is up at http://localhost:9090/

3. Check if Graphana is up at http://localhost:3000/

4. Inside cmd/terminal, run:
    a. docker network ls
    b. docker network inspect NETWORK_ID
        (where NETWORK_ID is the NETWORK ID of kafka-docker_default network)
    c. From the output, copy the IP address of the container named "kafka-docker-prometheus-1"

5. In Graphana, go to Home > Connections > Your connections > Data Sources > Prometheus

6. Paste the copied IP address inside the "URL" field

7. Run "docker compose up" inside the get-yt-chats directory

8. Inside cmd/terminal, run:
    a. docker network inspect NETWORK_ID
        (where NETWORK_ID is the NETWORK ID of kafka-docker_default network)
    b. From the output, copy the IP address of the container named "get-yt-chats-ytchats-1"

9. Paste the copied IP address inside static_configs > targets inside prometheus.yml

10. Restart containers inside kafka-docker by shutting down the containers manually in Docker Desktop and re-running "docker compose up" inside its directory

Resources:
https://github.com/jeanlouisboudart/kafka-platform-prometheus
https://www.datadoghq.com/blog/monitoring-kafka-performance-metrics/#kafka-producer-metrics
https://www.metricfire.com/blog/kafka-monitoring/
https://towardsdatascience.com/kafka-docker-python-408baf0e1088
docker run --rm -it --entrypoint sh f73c0d015bd8

Hardcoded values: 
1. prometheus targets in prometheus.yml
2. sentiment-analyzer IP in streamlit-app
3. prometheus datasource endpoint in grafana dashboard