from requests_html import HTMLSession, HTML
import time

session = HTMLSession()

web_url = "https://diemthi.vnexpress.net/tra-cuu-dai-hoc"

web_page: HTML = session.get(web_url).html # type: ignore

click_more_content_btn = """
  document.querySelector("div.lookup__footer > a.btn-outline").click()
"""

# web_page.render(script=click_more_content_btn, scrolldown=True, keep_page=True, reload=False, wait=1, sleep=1)
# web_page.render(script=click_more_content_btn, scrolldown=True)

a = web_page.find("div.lookup__footer", first=True).attrs.get('style')
while a is None:
  try:
    web_page.render(script=click_more_content_btn, scrolldown=True, keep_page=True, reload=False, wait=1, sleep=1)
  except:
    print("error")
  time.sleep(0.5)
  a = web_page.find("div.lookup__footer", first=True).attrs.get('style')

print(web_page.html)

