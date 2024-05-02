from bs4.element import Tag
from requests_html import HTML, Element, HTMLSession
from bs4 import BeautifulSoup

def parseSubject(link):
  return {
    'raw': link.attrs.get('title'),
    'code': link.text,
  }

def parseRow(row: Tag):
  columns = row.find_all("td")
  if (columns.__len__() < 7): return None

  subjectsInfo = list(map(parseSubject, columns[3].find_all("a")))

  return [
    columns[1].find("a").text, # name
    columns[1].find_all("span")[-1].text, # code
    columns[2].find("span").text, # entry point
    subjectsInfo, # subjects title
    columns[4].text, # fee
    columns[5].text, # note
  ]

def parseTable(table: str):
  web_page = BeautifulSoup(table, 'lxml')
  rows = web_page.find_all("tr", class_="university__benchmark") #type: ignore
  return list(filter(lambda ele: ele is not None, map(parseRow, rows)))

session = HTMLSession()

url = "https://diemthi.vnexpress.net/tra-cuu-dai-hoc/loadbenchmark/id/349/year/-1/sortby/1/block_name/all" 

respone = session.get(url).json()

html_raw = respone['html']

t = parseTable(html_raw)

toCsvInStdOut([
  "Tên",
  "Mã",
  "Điểm đầu vào",
  "Môn thi",
  "Học phí",
  "Ghi chú",
], t)

