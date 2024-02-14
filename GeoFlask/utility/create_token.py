import requests

login_url = "https://localhost:7042/api/v1/login"

# Replace these with the actual credentials
credentials = {
    "GokstadEmail": "johannes.andersen@gokstadakademiet.no",
    "Password": "MZHlhk54"
}

# Sending a POST request to the login endpoint with the credentials
response = requests.post(login_url, json=credentials, verify=False)  # verify=False is used to bypass SSL verification for testing

# Check if the login was successful
if response.ok:
    # Extract the token from the response
    token = response.text  # or response.json() if the API returns JSON
    print("Generated Token:", token)
else:
    print("Login failed:", response.text)
