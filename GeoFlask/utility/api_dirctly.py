import requests
import urllib3
import jwt
from datetime import datetime


urllib3.disable_warnings()

data = {
    "GokstadEmail": "anders.andersen@gokstadakademiet.no",     #Anders Andersen, anders.andersen@gokstadakademiet.no, VDMyxx15 (14)
    "Password": "VDMyxx15"
}
url = "https://localhost:7042/api/v1/Login"

response = requests.post(url, verify=False, json=data)
token = response.text
print("FIRST:", response.status_code)

url2 = "https://localhost:7042/api/v1/Assignment/1"                 # https://localhost:7042/api/v1/Event/User/14
headers = {"Authorization": f"Bearer {token}"}                      # https://localhost:7042/api/v1/Assignment/1
response = requests.get(url2, verify=False, headers=headers)

print("STATUSCODE:", response.status_code)
if response.ok:
    as_json = response.json()
    print(as_json)