from requests_html import HTML, HTMLSession
from time import sleep
from kafka import KafkaProducer

def takeThreadText(session: HTMLSession, kafka_producer: KafkaProducer, topic, board_url,  thread):
  replyLink = "/".join(thread.find("a.replylink", first=True).attrs['href'].split("/")[:2])
  link = board_url + "/" + topic + "/" + replyLink
  res = session.get(link) 
  kafka_producer.send(topic, res.text.encode("utf-8"))

def produce_page(session: HTMLSession, kafka_producer: KafkaProducer, topic, board_url,  page_num):
  page_url = "{url}/{topic}/{page_num}".format(url=board_url, topic=topic, page_num=page_num)

  res = session.get(page_url)
  htmlRes = HTML(html=res.text)
  threads = htmlRes.find(".thread")
  parseThreadInfoWith = lambda thread: takeThreadText(session, kafka_producer, topic,  board_url, thread)
  
  for thread in threads:
    parseThreadInfoWith(thread)

def produce_data(session: HTMLSession, board_url, topic):
  kafka_producer = KafkaProducer(bootstrap_servers='localhost:9092')
  produce_page(session, kafka_producer, topic, board_url, "")
  for page_num in range(2, 11):
    produce_page(session, kafka_producer, topic, board_url, page_num)


