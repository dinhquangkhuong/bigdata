from kafka import KafkaProducer 

kafka_producer = KafkaProducer(bootstrap_servers='localhost:9092')

for _ in range(3):
  kafka_producer.send("football", b"khuong hello world")

kafka_producer.flush()
