from kafka import KafkaConsumer
from parser import parseThreadInfo
from sys import argv

topic = argv[0]
assert topic != None, "must have a topic"

kafka_cusumer = KafkaConsumer(topic=topic, bootstrap_servers='localhost:9092')

for html_text in kafka_cusumer:
  parseThreadInfo()
  

