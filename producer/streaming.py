from math import floor
from parse import datetime
from requests_html import HTML, HTMLSession
from time import sleep
from kafka import KafkaProducer
import datetime

def takeThreadText(session: HTMLSession, kafka_producer: KafkaProducer, topic, board_url,  thread, timestamp_store):
  replyLink = "/".join(thread.find("a.replylink", first=True).attrs['href'].split("/")[:2])
  link = board_url + "/" + topic + "/" + replyLink
  res = session.get(link)
  utc_encode = "utc:" + str(timestamp_store['timestamp'])

  kafka_producer.send(topic + "streaming", utc_encode.encode("utf-8"))
  kafka_producer.send(topic + "streaming", res.text.encode("utf-8"))

def produce_page(session: HTMLSession, kafka_producer: KafkaProducer, topic, board_url,  page_num, timestamp_store):
  page_url = "{url}/{topic}/{page_num}".format(url=board_url, topic=topic, page_num=page_num)
  print(page_url)

  res = session.get(page_url)
  htmlRes = HTML(html=res.text)
  threads = htmlRes.find(".thread")
  parseThreadInfoWith = lambda thread: takeThreadText(session, kafka_producer, topic,  board_url, thread, timestamp_store)
  
  for thread in threads: # type: ignore
    parseThreadInfoWith(thread)

def produce_data(session: HTMLSession, board_url, topic):
  kafka_producer = KafkaProducer(bootstrap_servers='localhost:9092')
  timestamp_sotre = {
    'timestamp': floor(datetime.datetime.utcnow().timestamp()),
  }

  while True:
    produce_page(session, kafka_producer, topic, board_url, "", timestamp_sotre)

    for page_num in range(2, 4):
      produce_page(session, kafka_producer, topic, board_url, page_num, timestamp_sotre)

    timestamp_sotre = {
      'timestamp': floor(datetime.datetime.utcnow().timestamp()),
    }
    sleep(60)


