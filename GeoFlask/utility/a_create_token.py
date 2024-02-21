import requests

login_url = "https://localhost:7042/api/v1/login"

credentials = {
    "GokstadEmail": "johannes.andersen@gokstadakademiet.no",
    "Password": "MZHlhk54"
}

response = requests.post(login_url, json=credentials, verify=False)  # verify=False brukes for å bypasse "SSL verification" for testing

if response.ok:
    token = response.text
    print("Generated Token:", token)
else:
    print("Login failed:", response.text)
