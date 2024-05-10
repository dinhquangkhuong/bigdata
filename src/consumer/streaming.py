from math import floor
from kafka import KafkaConsumer
from consumer_parser import parseThreadInfo
from requests_html import HTMLSession
from threading import Thread
import datetime

def paserBoardLink(board_link):
  return "https:" + board_link.attrs['href']

session = HTMLSession()

org_url = "https://www.4chan.org/index.php"

org_page = session.get(org_url)
board_content = org_page.html.find(".boxcontent", first=True) # type: ignore

board_links = board_content.find("ul > li > a.boardlink") # type: ignore
board_urls = map(paserBoardLink, board_links) # type: ignore

def streaming_collect_data(topic, session: HTMLSession):
  kafka_cusumer = KafkaConsumer(topic + "streaming", bootstrap_servers='localhost:9092')
  timestamp_store = {
    'timestamp': floor(datetime.datetime.utcnow().timestamp())
  }

  for html_text in kafka_cusumer:
    html_decode = html_text.value.decode("utf-8")
    if html_decode.startswith("utc:"):
      timestamp_store['timestamp'] = int(html_decode[4:])
    else:
      print(parseThreadInfo(html_decode, session, utcPrev=timestamp_store['timestamp']))

for url in board_urls:
  topic = url.split("/")[-2]
  collect_topic = lambda : streaming_collect_data(topic, session)
  Thread(target=collect_topic).start()
  

