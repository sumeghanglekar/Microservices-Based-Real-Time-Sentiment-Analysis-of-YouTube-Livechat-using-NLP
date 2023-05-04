import time
import random
from os import path
from prometheus_client.core import GaugeMetricFamily, REGISTRY, CounterMetricFamily
from prometheus_client import start_http_server
totalRandomNumber = 0
class RandomNumberCollector(object):
    def __init__(self):
        pass
    def collect(self):
        gauge = GaugeMetricFamily("random_number", "A random number generator, I have no better idea", labels=["randomNum"])
        gauge.add_metric(['random_num'], random.randint(1, 20))
        yield gauge
        
        gauge1 = GaugeMetricFamily("random_number_1", "A random number generator, I have no better idea 1", labels=["randomNum1"])
        gauge1.add_metric(['random_num1'], random.randint(100, 200))
        yield gauge1
        

        count = CounterMetricFamily("random_number_2", "A random number 2.0", labels=['randomNum'])
        global totalRandomNumber
        totalRandomNumber += random.randint(1,30)
        count.add_metric(['random_num'], totalRandomNumber)
        yield count


if __name__ == "__main__":
    print("IN MAIN")
    start_http_server(9000)
    REGISTRY.register(RandomNumberCollector())
    while True:
        print("while loop")
        # period between collection
        time.sleep(1)