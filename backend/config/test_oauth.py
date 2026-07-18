import requests

url = (
    "https://accounts.zoho.in/oauth/v2/token"
    "?client_id=REMOVED_CLIENT_ID"
    "&client_secret=REMOVED_CLIENT_SECRET"
    "&grant_type=authorization_code"
    "&code=1000.00c3b5d37dd66aca139d6f247a86d46e.b478128ac013cc24264a68fa0cf65f03"
)

response = requests.post(url)

print(response.status_code)
print(response.text)