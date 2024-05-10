from requests_html import HTMLSession
from dotenv import load_dotenv
from os import getenv
from util.util_database import convertDataStr

load_dotenv(".env")

session = HTMLSession()

superset_url = getenv("SUPERSET_URL")
database_url = getenv("DATABASE_URL")

if superset_url is None:
  superset_url = "http://localhost:8088/"

login_api = "/api/v1/security/login"
post_database_api = "/api/v1/database"
assert database_url is not None, "database url not set"

database_data = convertDataStr(database_url)
database_data['expose_in_sqllab'] = True # type: ignore

def authUser(name: str, password):
  user = {
    "username": name,
    "password": password,
    "provider": "db",
    "refresh": True,
  }
  login_res = session.post(superset_url + login_api, json=user)

  jwt_token = login_res.json()['access_token']

  header_jwt = {
    "Authorization": f"Bearer {jwt_token}", 
  }

  csrf_token = session.get(
    url=superset_url + '/api/v1/security/csrf_token/',
    headers=header_jwt,
  ).json()["result"]

  return {
    'Accept': 'application/json',
    'X-CSRFToken': csrf_token,
    'Authorization': f'Bearer {jwt_token}',
  }

def createUserSkel(name: str, password: str):
  headers = authUser(name, password) 
  database_res = session.post(superset_url + "/api/v1/database", json=database_data, headers=headers)



