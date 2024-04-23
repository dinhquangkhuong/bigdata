from requests_html import HTMLSession
from kafka import KafkaConsumer
import subprocess

from customer_parser import parseThreadInfo

def paserBoardLink(board_link):
  return "https:" + board_link.attrs['href']

session = HTMLSession()

org_url = "https://www.4chan.org/index.php"

org_page = session.get(org_url)
board_content = org_page.html.find(".boxcontent", first=True) # type: ignore

board_links = board_content.find("ul > li > a.boardlink") # type: ignore
board_urls = map(paserBoardLink, board_links) # type: ignore

for url in board_urls:
  topic = url.split("/")[-2]
  subprocess.run(["./customer.sh", topic])

  
# for url in board_urls:
#   subprocess.run(["pkill", "customer-will-be-kill"])
