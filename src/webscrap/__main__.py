from bs4 import BeautifulSoup, Tag
from requests_html import AsyncHTMLSession, asyncio
from parser import toCsv, makeHeader
from threading import Thread


async def take(tag: Tag, year):
  session = AsyncHTMLSession()
  id = tag.attrs['href'].split('-')[-1]
  uni_name = tag.find("strong").text

  url = "https://diemthi.vnexpress.net/tra-cuu-dai-hoc/loadbenchmark/id/{id}/year/{year}/sortby/1/block_name/all".format(id=id, year=year)
  res = await session.get(url)
  html_raw = res.json()['html']
  toCsv(html_raw, uni_name, year)

  # with open(uni_data + '.csv', 'a', encoding='utf-8') as file:
  #   toCsv([
  #     "Tên",
  #     "Mã",
  #     "Điểm đầu vào",
  #     "Môn thi",
  #     "Học phí",
  #     "Ghi chú",
  #     ], html_raw, file)
  #   file.close()

async def fetchYear(tags, year):
  tasks = map(lambda tag: take(tag, year), tags)
  await asyncio.gather(*tasks)

async def main():
  with open("info.html", "r") as file:
    soup = BeautifulSoup(file.read(), "lxml")
    tags = soup.select("li.lookup__result > div.lookup__result-name > a")
    makeHeader()
    
    for year in [2019, 2020, 2021, 2022, 2023]:
      tasks = map(lambda tag: take(tag, year), tags)
      await asyncio.gather(*tasks)

    file.close()
      


asyncio.run(main())
    # break

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

