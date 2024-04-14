from time import sleep
from requests_html import HTML, HTMLSession
import json
# from requests_html import AsyncHTMLSession

session = HTMLSession()
url = "https://boards.4chan.org"
seed = "/a/"

current_url = url + seed
res = session.get(current_url)

htmlRes: HTML = res.html # type: ignore
boardList = htmlRes.find(".boardList", first=True)

tags = boardList.find("a")



def getPath(tag):
  return tag.attrs['href']

paths = map(getPath, tags)

threads = htmlRes.find(".thread")

def parseReplyReply(postMessageReplyTo):
  return postMessageReplyTo.text[2:]

def parseReplyInfo(reply):
  id = reply.attrs['id']
  postInfo = reply.find(".postInfo", first=True)
  userName = reply.find(".name", first=True).text
  dateTime = postInfo.find(".dateTime", first=True).text
  postMessage = reply.find(".postMessage", first=True)
  postMessageReplyTos = list(map(parseReplyReply, postMessage.find(".quotelink"))
  )
  postMessageText = postMessage.xpath("//blockquote/text()")

  return {
    'id': id,
    'usrName': userName,
    'postTime': dateTime,
    'postMess': postMessageText,
    'rep': postMessageReplyTos,
  }

def parseThreadInfo(thread):
  id = thread.attrs['id']
  postInfo = thread.find(".postInfo", first=True)

  userName = thread.find(".name", first=True).text
  subject = postInfo.find(".subject", first=True).text
  dateTime = postInfo.find(".dateTime", first=True).text
  postMessage = thread.find(".postMessage", first=True).text
  replyLink = thread.find(".replylink", first=True).attrs['href']
  repHtmlRes: HTML = session.get(current_url + replyLink).html # type: ignore

  sleep(0.5)
  repsList = repHtmlRes.find(".replyContainer")
  repsListInfo = list(map(parseReplyInfo, repsList))
  return {
    'id': id,
    'usrName': userName,
    'subj': subject,
    'postTime': dateTime,
    'postMess': postMessage,
    'repLink': replyLink,
    'repsList': repsListInfo,
  }

threadInfors = parseThreadInfo(threads[0])
# list(map(parseThreadInfo, threads))

with open("output-small.json", "w") as outfile:
  json.dump(threadInfors, outfile)

