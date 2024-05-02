from bs4 import BeautifulSoup, Tag
from requests_html import HTMLSession
from parser import parseToStdOut, toCsv
from threading import Thread

session = HTMLSession()

def take(tag: Tag):
  id = tag.attrs['href'].split('-')[-1]
  uni_name = "data/{uni_name}".format(uni_name=tag.find("strong").text)
  url = "https://diemthi.vnexpress.net/tra-cuu-dai-hoc/loadbenchmark/id/{id}/year/-1/sortby/1/block_name/all".format(id=id)
  html_raw = session.get(url).json()['html']
  with open(uni_name + '.csv', 'a', encoding='utf-8') as file:
    toCsv([
      "Tên",
      "Mã",
      "Điểm đầu vào",
      "Môn thi",
      "Học phí",
      "Ghi chú",
      ], html_raw, file)
    file.close()

with open("info.html", "r") as file:
  soup = BeautifulSoup(file.read(), "lxml")
  for tag in soup.select("li.lookup__result > div.lookup__result-name > a"):
    run_thread = lambda : take(tag)
    Thread(target=run_thread).start()

# url = "https://diemthi.vnexpress.net/tra-cuu-dai-hoc/loadbenchmark/id/349/year/-1/sortby/1/block_name/all" 
#
# respone = session.get(url).json()
#
# html_raw = respone['html']
#
#
# print(
# toCsv([
#   "Tên",
#   "Mã",
#   "Điểm đầu vào",
#   "Môn thi",
#   "Học phí",
#   "Ghi chú",
#   ], html_raw)
# )

