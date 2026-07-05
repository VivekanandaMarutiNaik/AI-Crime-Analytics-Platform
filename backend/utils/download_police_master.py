import requests
import time
import os

url = "https://ksp.karnataka.gov.in/home-fetch"
os.makedirs("datasets/police/raw", exist_ok=True)

for district_id in range(9, 42):

    params = {
        "select": "district_id",
        "value": district_id,
        "dependent": "district_row_id"
    }

    response = requests.get(url, params=params)
    time.sleep(1)

    with open(
        f"datasets/police/raw/district_{district_id}.html",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(response.text)

    print(
        f"District {district_id}: "
        f"Status {response.status_code} | "
        f"{len(response.text)} characters"
    )