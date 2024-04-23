from kafka import KafkaConsumer
from customer_parser import parseThreadInfo
from sys import argv

topic = argv[1]
assert topic != None, "must have a topic"

kafka_cusumer = KafkaConsumer(topic, bootstrap_servers='localhost:9092')

for html_text in kafka_cusumer:
  print(parseThreadInfo(html_text.value.decode("utf-8")))
  

