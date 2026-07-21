import requests

CLIENT_ID = "1000.C0PXT4W5XSN0YJTQTCINVY5QXVB9QS"
CLIENT_SECRET = "5bbc2c85abd615072e38a418dbc31997e413756f0f"


REFRESH_TOKEN = "1000.9b5ae46007e844af83d9a957f025a8c1.90c332f152c5568ffa1cc22af786ce62"

url = "https://accounts.zoho.in/oauth/v2/token"

payload = {
    "refresh_token": REFRESH_TOKEN,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "grant_type": "refresh_token",
}

response = requests.post(url, data=payload)

print(response.status_code)
print(response.json())