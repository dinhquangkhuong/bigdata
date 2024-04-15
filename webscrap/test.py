from requests_html import HTMLSession, HTML
import load_page

session = HTMLSession()
url = "https://boards.4chan.org/a/thread/265453391"
res = session.get(url)

# res.html.render(scrolldown=5,sleep=0.1)
html = HTML(html=res.text)

threads = html.find(selector="div.replyContainer")
for thread in threads:
  print(thread)

parse = lambda reply: load_page.parseReplyInfo(reply)

threads_parsed = list(map(parse, threads)).__len__()
print(threads_parsed)
# print(threads_parsed)
# for val in threads_parsed:
#   print(val)

