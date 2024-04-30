from requests_html import HTMLSession
from dotenv import load_dotenv
from os import getenv
import util

load_dotenv(".env")

session = HTMLSession()

url = "http://localhost:8088"

database_url = getenv("DATABASE_URL") 



database_data = {
  "database_name": "bigdata",
  "username": "khuong",
  "password": "12",
  "expose_in_sqllab": True,
  "sqlalchemy_uri": database_url
}

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

post_database_api = url + "/api/v1/database"
print(post_database_api)


database_res = session.post(post_database_api,
                             json=database_data,
                             headers=headers)

