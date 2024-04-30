from requests_html import HTMLSession
from threading import Thread
from streaming import produce_data

def paserBoardLink(board_link):
  return "https:" + board_link.attrs['href']

session = HTMLSession()

org_url = "https://www.4chan.org/index.php"

org_page = session.get(org_url)
board_content = org_page.html.find(".boxcontent", first=True) # type: ignore

board_links = board_content.find("ul > li > a.boardlink") # type: ignore
board_urls = map(paserBoardLink, board_links) # type: ignore

main_url = "https://boards.4chan.org"

# def produce_data(session: HTMLSession, board_url, topic):
produce_data_session = lambda topic: produce_data(session, main_url, topic) 
for url in board_urls:
  topic = url.split("/")[-2]
  produce_data_session_topic = lambda : produce_data_session(topic)
  Thread(target=produce_data_session_topic).start()


