import requests

url = "https://ksp.karnataka.gov.in/pslocator/en"

response = requests.get(url, timeout=30)

print("Status:", response.status_code)

with open("datasets/police/raw/main_page.html", "w", encoding="utf-8") as f:
    f.write(response.text)

print("Saved main_page.html")