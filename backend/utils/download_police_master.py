import requests
import time

url = "https://ksp.karnataka.gov.in/home-fetch"

for district_id in range(34, 42):

    params = {
        "select": "district_id",
        "value": district_id,
        "dependent": "district_row_id"
    }

    response = requests.get(url, params=params)
    time.sleep(1)
    print(
        f"District {district_id}: "
        f"Status {response.status_code} | "
        f"{len(response.text)} characters"
    )