from math import floor
from requests_html import HTML, HTMLSession
import datetime

def getPath(tag):
  return tag.attrs['href']

def parseReplyReply(postMessageReplyTo):
  return postMessageReplyTo.text[2:]

def parseReplyInfo(reply, utcTime=None):
  id = reply.attrs['id']
  postInfo = reply.find(".postInfo", first=True)
  dateTime = postInfo.find(".dateTime", first=True)
  replyDateTimeUTC = int(dateTime.attrs['data-utc'])

  if utcTime and utcTime < replyDateTimeUTC:
    return {
      'id': id,
      'old': True,
    } 

  userName = reply.find(".name", first=True).text
  postMessage = reply.find(".postMessage", first=True)
  postMessageReplyTos = list(map(parseReplyReply, postMessage.find(".quotelink")))

  postMessageText = postMessage.xpath("//blockquote/text()")

  return {
    'id': id,
    'usrName': userName,
    'postTime': dateTime.text,
    'postMess': postMessageText,
    'rep': postMessageReplyTos,
    'old': False, 
  }

def parseThreadInfo(html_text, session: HTMLSession, utcPrev=None):
  thread_html = HTML(session=session, html=html_text)

  thread = thread_html.find("div.thread", first=True)
  id = thread.attrs['id']
  postInfo = thread_html.find(".postInfo", first=True)

  userName = thread_html.find(".name", first=True).text
  subject = postInfo.find(".subject", first=True)
  dateTime = postInfo.find(".dateTime", first=True)
  utcTime = int(dateTime.attrs['data-utc'])
  postMessage = thread_html.find(".postMessage", first=True).text

  repsList = thread_html.find(".replyContainer")
  parseReplyInfoUTC = lambda reply: parseReplyInfo(reply, utcPrev)
  oldThread = utcPrev is None and utcPrev < utcTime

  repsListInfo = list(map(parseReplyInfoUTC, repsList)) # type: ignore
  utc_timestamp = floor(datetime.datetime.utcnow().timestamp()) 
  print(utc_timestamp, utcPrev)

  return {
    'id': id,
    'usrName': userName,
    'subj': subject,
    'postTime': dateTime.text,
    'postMess': postMessage,
    'repsList': repsListInfo,
    'old': oldThread
  }

