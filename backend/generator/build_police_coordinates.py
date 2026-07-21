import re
import pandas as pd
from rapidfuzz import process, fuzz

POLICE_FILE = "datasets/processed/police_master.csv"
PLACES_FILE = "datasets/raw/karnataka_places_filtered.csv"
OUTPUT_FILE = "datasets/processed/police_master_geocoded_new.csv"

police = pd.read_csv(POLICE_FILE)
places = pd.read_csv(PLACES_FILE)



def clean(text):
    text = str(text).lower()

    remove = [
        "police station",
        "ps",
        "traffic",
        "women",
        "rural",
        "town",
        "city",
        "cen crime",
        "crime",
        "north",
        "south",
        "east",
        "west",
        "sub urban",
        "sub-urban",
        "suburban",
        "apmc",
        "yard",
        "market",
        "bazar",
        "bazar",
        "mohalla",
        
    ]

    for word in remove:
        text = text.replace(word, " ")

    text = re.sub(r"[^a-z ]", " ", text)
    text = " ".join(text.split())
    # Common Karnataka spelling normalization
    replacements = {
        "bellary": "ballari",
        "hubli": "hubballi",
        "hungunda": "hunagunda",
        "lakshmeshwar": "lakshmeshvara",
        "mulbagal": "mulabagilu",
        "nargund": "naragunda",
        "mundargi": "mundaragi",
        "mulagund": "mulagunda",
        "halebeedu": "hulebeedu",
        "amengad": "aminagada",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


places["clean_name"] = places["name"].apply(clean)
police["clean_name"] = police["police_station_name"].apply(clean)

print("Police stations :", len(police))
print("OSM places      :", len(places))

# Build lookup
# Prefer towns over villages when duplicate names exist
places = places.sort_values(
    by="fclass",
    key=lambda s: s.map({"town": 0, "village": 1}).fillna(2)
)

place_lookup = {
    row["clean_name"]: row
    for _, row in places.drop_duplicates(subset=["clean_name"], keep="first").iterrows()
}

matched = []
manual = []

for _, row in police.iterrows():

    station = row["clean_name"]

    # ---------- Exact Match ----------
    if station in place_lookup:

        p = place_lookup[station]

        

        matched.append({
            **row.to_dict(),
            "latitude": p["Y"],
            "longitude": p["X"],
            "match_type": "EXACT"
        })

        continue

    # ---------- Fuzzy Match ----------
    result = process.extractOne(
        station,
        place_lookup.keys(),
        scorer=fuzz.WRatio
    )

    if result and result[1] >= 87:

        p = place_lookup[result[0]]

        matched.append({
            **row.to_dict(),
            "latitude": p["Y"],
            "longitude": p["X"],
            "match_type": f"FUZZY ({result[1]:.1f})"
        })

    else:
        matched.append({
            **row.to_dict(),
            "latitude": row["latitude"],
            "longitude": row["longitude"],
            "match_type": "ORIGINAL"
        })

        manual.append({
            "district": row["ksp_district"],
            "police_station": row["police_station_name"],
            "best_match": result[0] if result else "",
            "score": result[1] if result else 0,
        })

print(f"Matched : {len(matched)}")
print(f"Manual  : {len(manual)}")

matched_df = pd.DataFrame(matched)
manual_df = pd.DataFrame(manual)

matched_df.to_csv(
    "datasets/processed/police_master_geocoded_new.csv",
    index=False
)

manual_df.to_csv(
    "datasets/processed/manual_review.csv",
    index=False
)

print("Files saved successfully.")