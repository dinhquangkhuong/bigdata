from kafka import KafkaConsumer

kafka_consumer = KafkaConsumer("football", bootstrap_servers='localhost:9092')

for msg in kafka_consumer:
  print(msg)
