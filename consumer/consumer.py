from kafka import KafkaConsumer
from consumer_parser import parseThreadInfo

def collect_data(topic):
  kafka_cusumer = KafkaConsumer(topic, bootstrap_servers='localhost:9092')

  for html_text in kafka_cusumer:
    print(parseThreadInfo(html_text.value.decode("utf-8")))
  

