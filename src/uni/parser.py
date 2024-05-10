from json import JSONEncoder
from typing import Any, List
from bs4.element import Tag
from bs4 import BeautifulSoup
from lxml.html import LabelElement

jsonEn = JSONEncoder(ensure_ascii=False)

# def __printOne__(values: List[Any]):
#   for value in values[:-1]:
#     print("\"", value, "\",", sep="",end="")
#
#   print("\"", values[-1], "\"")
#
# def toCsvInStdOut(headers: List[str], values: List[List[str]]):
#   __printOne__(headers)
#
#   for value in values:
#     __printOne__(value)
#
# def parseToStdOut(raw):
#   t = parseTable(raw)
#   uni_data = list(map(lambda i: i[0], t))
#   uni_subject = list(map(lambda i: i[1], t))
#
#   toCsvInStdOut([
#     "Tên",
#     # "Mã",
#     "Điểm đầu vào",
#     "Môn thi",
#     "Học phí",
#     "Ghi chú",
#   ], uni_data)

def parseSubject(link):

  return {
    'raw': link.attrs.get('title'), # vd: ['anh, toán, lí', ...]
    'code': link.text, # vd: A01, C01, ... 
  }

def parseRow(row: Tag, uni_name):
  columns = row.find_all("td")
  if (columns.__len__() < 7): return None

  subjectsInfo = list(map(parseSubject, columns[3].find_all("a")))
  subject_name = columns[1].find_all("a")[0].text
  subject_code = columns[1].find_all("span")[-1].text

  return [
    [
      uni_name,
      subject_code, # code
      subject_name,
      columns[2].find("span").text, # entry point
      columns[4].text, # fee
      columns[5].text, # note
    ],
    [
      uni_name,
      subject_code,
      subject_name,
      subjectsInfo, # subjects title
    ]
  ]

def parseTable(table: str, uni_name):
  web_page = BeautifulSoup(table, 'lxml')
  rows = web_page.find_all("tr", class_="university__benchmark") #type: ignore
  parseRowAlt = lambda row: parseRow(row, uni_name=uni_name)
  return list(filter(lambda ele: ele is not None, map(parseRowAlt, rows)))


def __oneLine__(values: List[str], file):
  for value in values[:-1]:
    print("\"", value, "\",", sep="",end="", file=file)

  print("\"", values[-1], "\",", sep="", file=file)

headers = [
  "university",
  "subject_code",
  "subject_name",
  "entry_point",
  "fee",
  "note",
]

subject_code_header = [
  "university",
  "subject_code",
  "subject_raw",
]


def makeHeader():
  # uni_data = "university_data/{uni_name}".format(uni_name=uni_name)
  uni_subject = "university_subject/1_header"
  uni_subject_code = "university_subject_code/1_header"

  # uni_data_f = open(uni_data + '.csv', 'a', encoding='utf-8')
  uni_subject_f = open(uni_subject + '.csv', 'a', encoding='utf-8')
  uni_subject_code_f = open(uni_subject_code + '.csv', 'a', encoding='utf-8')

  __oneLine__(headers, uni_subject_f)
  __oneLine__(subject_code_header, uni_subject_code_f)

  uni_subject_code_f.close()
  uni_subject_f.close()


def toCsv(html_raw: str, uni_name):
  table = parseTable(html_raw, uni_name)
  uni_data_raw = list(map(lambda i: i[0], table))
  uni_subject_raw = list(map(lambda i: i[1], table))

  # uni_data = "university_data/{uni_name}".format(uni_name=uni_name)
  uni_subject = "university_subject/{uni_name}".format(uni_name=uni_name)
  uni_subject_code = "university_subject_code/{uni_name}".format(uni_name=uni_name)

  # uni_data_f = open(uni_data + '.csv', 'a', encoding='utf-8')
  uni_subject_f = open(uni_subject + '.csv', 'a', encoding='utf-8')
  uni_subject_code_f = open(uni_subject_code + '.csv', 'a', encoding='utf-8')


  # __oneLine__(headers, uni_subject_f)
  for value in uni_data_raw:
    __oneLine__(value, uni_subject_f)

  # __oneLine__(subject_code_header, uni_subject_code_f)
  for value in uni_subject_raw:
    __oneLine__(value, uni_subject_code_f)

  # uni_data_f.close()
  uni_subject_f.close()
  uni_subject_code_f.close()


# session = HTMLSession()
#
# url = "https://diemthi.vnexpress.net/tra-cuu-dai-hoc/loadbenchmark/id/349/year/-1/sortby/1/block_name/all" 
#
# respone = session.get(url).json()
#
# html_raw = respone['html']
#
# t = parseTable(html_raw)
#
# toCsvInStdOut([
#   "Tên",
#   "Mã",
#   "Điểm đầu vào",
#   "Môn thi",
#   "Học phí",
#   "Ghi chú",
# ], t)
#
