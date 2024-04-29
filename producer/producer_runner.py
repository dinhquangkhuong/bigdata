from requests_html import HTMLSession
import subprocess

def paserBoardLink(board_link):
  return "https:" + board_link.attrs['href']

session = HTMLSession()

org_url = "https://www.4chan.org/index.php"

org_page = session.get(org_url)
board_content = org_page.html.find(".boxcontent", first=True) # type: ignore

board_links = board_content.find("ul > li > a.boardlink") # type: ignore
board_urls = map(paserBoardLink, board_links) # type: ignore

main_url = "https://boards.4chan.org"

for url in board_urls:
  topic = url.split("/")[-2]
  subprocess.Popen(["./producer.sh", main_url, topic])
  # produce_non_archive(session, main_url, "a")
  # break


