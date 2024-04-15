from requests_html import HTML

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

def parseThreadInfo(html_text):
  thread_html = HTML(html=html_text)
  id = thread_html.find(".thread", first=True).attrs['id'][1::]
  
  postInfo = thread_html.find(".postInfo", first=True)

  userName = thread_html.find(".name", first=True).text
  subject = postInfo.find(".subject", first=True).text
  dateTime = postInfo.find(".dateTime", first=True).text
  postMessage = thread_html.find(".postMessage", first=True).text
  replyLink = thread_html.find(".replylink", first=True).attrs['href']

  repsList = thread_html.find(".replyContainer")
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

