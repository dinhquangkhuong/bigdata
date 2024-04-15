from requests_html import HTML, HTMLSession

def getPath(tag):
  return tag.attrs['href']

def parseReplyReply(postMessageReplyTo):
  return postMessageReplyTo.text[2:]

def parseReplyInfo(reply):
  id = reply.attrs['id']
  postInfo = reply.find(".postInfo", first=True)
  userName = reply.find(".name", first=True).text
  dateTime = postInfo.find(".dateTime", first=True).text
  postMessage = reply.find(".postMessage", first=True)
  postMessageReplyTos = map(parseReplyReply, postMessage.find(".quotelink"))

  postMessageText = postMessage.xpath("//blockquote/text()")

  return {
    'id': id,
    'usrName': userName,
    'postTime': dateTime,
    'postMess': postMessageText,
    'rep': postMessageReplyTos,
  }

def parseThreadInfo(session: HTMLSession, current_url, thread):
  id = thread.attrs['id']
  postInfo = thread.find(".postInfo", first=True)

  userName = thread.find(".name", first=True).text
  subject = postInfo.find(".subject", first=True).text
  dateTime = postInfo.find(".dateTime", first=True).text
  postMessage = thread.find(".postMessage", first=True).text
  replyLink = thread.find(".replylink", first=True).attrs['href']
  res = session.get(current_url + replyLink) 
  repHtmlRes = HTML(html=res.text)

  repsList = repHtmlRes.find(".replyContainer")
  repsListInfo = list(map(parseReplyInfo, repsList)) # type: ignore

  return {
    'id': id,
    'usrName': userName,
    'subj': subject,
    'postTime': dateTime,
    'postMess': postMessage,
    'repLink': replyLink,
    'repsList': repsListInfo,
  }

def load_page(session: HTMLSession, page_url):
  res = session.get(page_url)
  htmlRes = HTML(html=res.text)
  threads = htmlRes.find(".thread")
  parseThreadInfoWith = lambda thread: parseThreadInfo(session, page_url, thread)
  return list(map(parseThreadInfoWith, threads)) # type: ignore
  # return parseThreadInfoWith(threads[0])


