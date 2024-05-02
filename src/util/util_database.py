# from typing import Any, List
#
# def __printOne__(values: List[Any]):
#   for value in values[:-1]:
#     print("\"", value, "\",")
#
#   print("\"", values[-1], "\"")
#
#
# def toCsvInStdOut(headers: List[str], values: List[List[Any]]):
#   __printOne__(headers)
#
#   for value in values:
#     __printOne__(value)
#

def convertDataStr(databseUrl: str):
  splitProtocol = databseUrl.split("://")
  splitDatabase = splitProtocol[1].split("/")
  database_name = splitDatabase[-1]
  splitUrl = splitDatabase[0].split("@")
  splitUser = splitUrl[0].split(":")

  userName = splitUser[0]
  userPassword = splitUser[1]
  # dbProtocol = splitProtocol[0]

  # splitIp = splitUrl[1].split(":")
  #
  # ipaddress = splitIp[0]
  # port = splitIp[1]

  # print(dbProtocol, database_name, userName, userPassword, ipaddress, port)
  return {
    "database_name": database_name,
    "username": userName,
    "password": userPassword,
    "sqlalchemy_uri": databseUrl
  }

