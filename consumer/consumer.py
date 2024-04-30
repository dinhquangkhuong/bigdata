from kafka import KafkaConsumer
from consumer_parser import parseThreadInfo
from requests_html import HTMLSession
# import psycopg2

# conn = psycopg2.connect("postgres://khuong:12@127.0.0.1:5432/bigdata")

# cur = conn.cursor()
#
# cur.execute("SELECT * FROM public.user LIMIT 20")
#
# records = cur.fetchall()
# print(records)


def collect_data(topic: str, session: HTMLSession):
  kafka_cusumer = KafkaConsumer(topic, bootstrap_servers='localhost:9092')

  for html_text in kafka_cusumer:
    print(parseThreadInfo(html_text.value.decode("utf-8"), session, None))
  

