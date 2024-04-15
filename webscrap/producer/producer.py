from requests_html import HTML, HTMLSession
from kafka import KafkaProducer

def takeThreadText(session: HTMLSession, producer: KafkaProducer, page_url, topic , thread):
  replyLink = thread.find(".replylink", first=True).attrs['href']
  res = session.get(page_url + replyLink) 
  producer.send(topic=topic,value=res.text)

def produce_page(session: HTMLSession, url, topic):
  kafka_producer = KafkaProducer(bootstrap_servers='localhost:9092')
  page_url = "{url}{topic}".format(url, topic)

  res = session.get(page_url)
  htmlRes = HTML(html=res.text)
  threads = htmlRes.find(".thread")
  parseThreadInfoWith = lambda thread: takeThreadText(session, kafka_producer,  page_url, topic, thread)
  map(parseThreadInfoWith, threads) # type: ignore
  # return parseThreadInfoWith(threads[0])


