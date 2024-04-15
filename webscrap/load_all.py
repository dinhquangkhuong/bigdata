import json
from requests_html import Element, HTMLSession
from load_page import load_page

def paserBoardLink(board_link):
  return "https:" + board_link.attrs['href']

session = HTMLSession()

org_url = "https://www.4chan.org/index.php"

org_page = session.get(org_url)
board_content: Element = org_page.html.find(".boxcontent", first=True) # type: ignore

board_links = board_content.find("ul > li > a.boardlink") # type: ignore
board_urls = map(paserBoardLink, board_links) # type: ignore

with open("test-all.json", "a") as outfile:
  for url in board_urls:
      for i in range(1, 11):
        page_url = "{url}{page_num}".format(url=url, page_num=i)
        json.dump(load_page(session, page_url), outfile)
        outfile.write("\n")
  outfile.close()


