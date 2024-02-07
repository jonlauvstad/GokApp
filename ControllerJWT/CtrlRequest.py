import requests
import urllib3
import jwt
from datetime import datetime


urllib3.disable_warnings()

data = {
    "GokstadEmail": "a.m@gokstad.com",      #"a.l@gokstad.com"
    "Password": "Tann1000#"                  #"Jon1000#"
}

response = requests.post(f"https://localhost:7253/api/v1/Login", verify=False, json=data)
print("Post-request to get token:")
print(response)
print(response.status_code)
print(response.content)
print(response.text)

token = response.text
decoded_token = jwt.decode(token, options={'verify_signature': False})
expiration = decoded_token['exp']
expiration_datetime = datetime.utcfromtimestamp(expiration)
identifier = decoded_token['idf']
adm = decoded_token.get("adm")
id = decoded_token['id']
print(identifier, adm, id)
print(expiration_datetime)
print("decoded_token:", decoded_token)
print()


headers = {"Authorization": f"Bearer {token}"}
response = requests.get(f"https://localhost:7253/api/v1/User/1", verify=False, headers=headers)
print("Get-request using token in Authorization-header:")
print(response, response.status_code, response.content, response.text)
