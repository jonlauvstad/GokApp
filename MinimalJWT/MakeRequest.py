import requests
import urllib3
import jwt
from datetime import datetime


urllib3.disable_warnings()

# endpoint = ".../api/ip"
# data = {"ip": "1.1.2.3"}

jwt_token = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJJZCI6ImY1M2QzN2ZkLTQ5MzQtNDhmNC05YTZhLTFjOWUzZmU0NzYwMyIsInN1YiI6ImJhbGxlLmtsb3JpbkBnbWFpbC5jb20iLCJlbWFpbCI6ImJhbGxlLmtsb3JpbkBnbWFpbC5jb20iLCJqdGkiOiI5NTE1MDczMS03YWNiLTQ3MTMtYmYzMy1kZjkwZTcwNDQyOWEiLCJyb2xlIjoiZmFsc2UiLCJuYmYiOjE3MDQ0MzYxMjIsImV4cCI6MTcwNDQzNjQyMiwiaWF0IjoxNzA0NDM2MTIyLCJpc3MiOiJodHRwczovL2pveWRpcGthbmppbGFsLmNvbS8iLCJhdWQiOiJodHRwczovL2pveWRpcGthbmppbGFsLmNvbS8ifQ.tZB-2gbWftMG4jJ8lT03VN96Mt6x38KFZpzJ2F59yk-nfVgRZjRitcABKBwC8IRiF_zqokCSznkOoX1mMQbGXg"
try:
    decoded_token = jwt.decode(jwt_token, options={'verify_signature': False})      # var False
    # user_id = decoded_token['user_id']
    username = decoded_token['sub']
    expir = decoded_token['exp']
    expiration_datetime = datetime.utcfromtimestamp(expir)
    role = decoded_token['role']

    # print(f"User ID: {user_id}")
    print(f"Username: {username}")
    print(expiration_datetime)
    print(role)

except jwt.ExpiredSignatureError:
    print("Token has expired.")
except jwt.InvalidTokenError:
    print("Invalid token.")



# headers = {"Authorization": "Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJJZCI6ImExOGNiN2NhLWVjNzAtNDUwOC05ZmRiLWU5YzNiMjMwY2E1MiIsInN1YiI6ImpveWRpcCIsImVtYWlsIjoiam95ZGlwIiwianRpIjoiZjUzMWVlZWYtODZiYy00NjkwLThjYmEtZjI2NTJkMTk1NDA3IiwibmJmIjoxNzA0MzcxMTMxLCJleHAiOjE3MDQzNzE0MzEsImlhdCI6MTcwNDM3MTEzMSwiaXNzIjoiaHR0cHM6Ly9qb3lkaXBrYW5qaWxhbC5jb20vIiwiYXVkIjoiaHR0cHM6Ly9qb3lkaXBrYW5qaWxhbC5jb20vIn0.PXLU7tGJeiG57okaXRQOfZuREWHxDWVp40LW6AFKweVzosaL79JkA8vqQNNKqwHRAJwFLXSmWunY-SFp3sySTw"}
headers = {"Authorization": f"Bearer {jwt_token}"}


response = requests.get(f"https://localhost:7020/security/getMessage", verify=False, #json=data,
                            headers=headers)
print(response)
print(response.content)
print(response.status_code)
try:
    response = response.json()
except:
    response = response.text
print(response)


