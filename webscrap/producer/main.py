from kafka import KafkaProducer
from requests_html import HTMLSession

org_url = "https://www.4chan.org/index.php"

kafka_producer = KafkaProducer(bootstrap_servers='localhost:9092')
session = HTMLSession()

org_page = session.get(org_url)

kafka_producer.send(topic="main-board-url", value=org_page.text)


