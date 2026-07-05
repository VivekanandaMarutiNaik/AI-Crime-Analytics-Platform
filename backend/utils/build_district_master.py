from bs4 import BeautifulSoup
import pandas as pd
import os

with open("datasets/police/raw/main_page.html", encoding="utf-8") as f:
    soup = BeautifulSoup(f.read(), "html.parser")

district_select = soup.find("select", id="district_id")

rows = []

for option in district_select.find_all("option"):

    district_id = option.get("value", "").strip()
    district_name = option.text.strip()

    if district_id == "" or district_id == "0":
        continue

    rows.append({
        "district_id": int(district_id),
        "district_name": district_name
    })

df = pd.DataFrame(rows)

os.makedirs("datasets/processed", exist_ok=True)

df.to_csv(
    "datasets/processed/district_master.csv",
    index=False
)

print(df)

print("\nTotal Districts:", len(df))