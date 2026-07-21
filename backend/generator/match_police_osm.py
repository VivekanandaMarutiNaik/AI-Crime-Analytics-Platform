import re
import pandas as pd
from rapidfuzz import process, fuzz

POLICE_FILE = "datasets/processed/police_master.csv"
OSM_FILE = "datasets/raw/karnataka_places.csv"

police = pd.read_csv(POLICE_FILE)
osm = pd.read_csv(OSM_FILE)


def clean_name(name):
    name = str(name).lower()

    # Remove common police suffixes
    remove_words = [
        "police station",
        "ps",
        "traffic",
        "women",
        "rural",
        "town",
        "city",
        "cen crime",
        "crime",
    ]

    for word in remove_words:
        name = name.replace(word, " ")

    # Keep only letters and spaces
    name = re.sub(r"[^a-z ]", " ", name)

    # Remove extra spaces
    name = " ".join(name.split())

    return name


osm["clean_name"] = osm["name"].apply(clean_name)
police["clean_name"] = police["police_station_name"].apply(clean_name)
osm_names = osm["clean_name"].tolist()
# Test matching on first 20 police stations

unmatched = []

for _, row in police.iterrows():

    match = process.extractOne(
        row["clean_name"],
        osm_names,
        scorer=fuzz.WRatio
    )

    if not match or match[1] < 90:
        unmatched.append({
            "district": row["ksp_district"],
            "police_station": row["police_station_name"],
            "clean_name": row["clean_name"],
            "best_match": match[0] if match else "",
            "score": match[1] if match else 0,
        })

unmatched_df = pd.DataFrame(unmatched)
unmatched_df.to_csv("datasets/processed/unmatched_police.csv", index=False)

print(unmatched_df.head(30))
print(f"\nTotal unmatched: {len(unmatched_df)}")