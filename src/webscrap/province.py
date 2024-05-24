from bs4.element import Tag
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd

session = HTMLSession()

url = 'https://vi.wikipedia.org/wiki/ISO_3166-2:VN'

res = session.get(url)

html = BeautifulSoup(res.content.decode("utf-8"))

table = html.select("div.mw-content-ltr > table.wikitable > tbody > tr")

def parseTable(tag: Tag):
  cols = tag.select("td")
  if cols.__len__() < 2:
    return None

  return {
    'iso': cols[0].text.strip("\n"),
    'name': cols[1].text.strip("\n")
  }

provinces = list(filter(lambda val: val is not None, map(parseTable, table)))

df = pd.DataFrame(provinces)

df.to_csv("test.csv")






