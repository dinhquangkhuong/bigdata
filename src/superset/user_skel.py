from requests_html import HTMLSession
from dotenv import load_dotenv
from os import getenv
from util.util_database import convertDataStr

load_dotenv(".env")

session = HTMLSession()

url = "http://localhost:8088"
login_api = "/api/v1/security/login"
post_database_api = "/api/v1/database"

database_url = getenv("DATABASE_URL") 

assert database_url is not None, "database url not set"
database_data = convertDataStr(database_url)
database_data['expose_in_sqllab'] = True # type: ignore

# { 
#   "database_name": "bigdata",
#   "username": "khuong",
#   "password": "12",
#   "expose_in_sqllab": True,
#   "sqlalchemy_uri": database_url
# }

user = {
  "username": "admin",
  "password": "admin",
  "provider": "db",
  "refresh": True,
}

login_res = session.post(url + login_api, json=user)

jwt_token = login_res.json()['access_token']

header_jwt = {
  "Authorization": f"Bearer {jwt_token}", 
}

csrf_token = session.get(
  url=url + '/api/v1/security/csrf_token/',
  headers=header_jwt,
).json()["result"]


data_data = {
  'csrftoken': csrf_token,
}

headers = {
  'Accept': 'application/json',
  'X-CSRFToken': csrf_token,
  'Authorization': f'Bearer {jwt_token}',
}

database_res = session.post(url + "/api/v1/database", json=database_data, headers=headers)

