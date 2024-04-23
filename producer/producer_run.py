from sys import argv
from requests_html import HTMLSession

from producer import produce_non_archive

board_url = argv[1]
assert board_url != None, "init board_url"
topic = argv[2]
assert topic != None, "init topic"

print(board_url, topic)
session = HTMLSession()
produce_non_archive(session, board_url, topic)
