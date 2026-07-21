import random
from pathlib import Path
from backend.generator.rules import (
    get_random_crime,
    get_victim_gender,
    get_crime_severity,
    get_fir_status,
    get_response_time,
    get_cctv_availability,
    get_time_slot,
)
import pandas as pd
from faker import Faker

fake = Faker("en_IN")
NUM_RECORDS = 50000

from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[2]

LOCATION_MASTER = pd.read_csv(
    BASE_DIR / "datasets" / "processed" / "village_coordinates.csv"
)

# -----------------------------
# District-wise weighted sampling
# -----------------------------

DISTRICT_GROUPS = {}

for district, df in LOCATION_MASTER.groupby("district_name"):

    df = df.copy()

    # Count villages per taluk
    taluk_counts = (
        df.groupby("taluk_name")
        .size()
        .sort_values(ascending=False)
    )

    # Larger taluks receive higher probability
    taluk_weights = (
        taluk_counts / taluk_counts.sum()
    ).to_dict()

    DISTRICT_GROUPS[district] = {
        "villages": df,
        "weights": taluk_weights,
    }

# District weights based on number of villages
district_counts = (
    LOCATION_MASTER.groupby("district_name")
    .size()
)

DISTRICT_NAMES = district_counts.index.tolist()
DISTRICT_WEIGHTS = district_counts.values.tolist()


crime_records = []

# Create a pool of repeat offenders
OFFENDERS = [
    f"ACC{str(i).zfill(5)}"
    for i in range(1, 501)
]

used_crime_ids = set()

for i in range(NUM_RECORDS):

    # Pick one random location
    # 70% of crimes happen in hotspot villages
    # Choose a district first
    district = random.choices(
    DISTRICT_NAMES,
    weights=DISTRICT_WEIGHTS,
    k=1,
)[0]

    district_df = DISTRICT_GROUPS[district]["villages"]

    taluk_weights = DISTRICT_GROUPS[district]["weights"]

    taluks = list(taluk_weights.keys())
    weights = list(taluk_weights.values())

    # Choose taluk according to weight
    selected_taluk = random.choices(
        taluks,
        weights=weights,
        k=1,
    )[0]

    taluk_df = district_df[
        district_df["taluk_name"] == selected_taluk
    ]

    # Choose village inside taluk
    location = taluk_df.sample(1).iloc[0]

    # Generate hotspot score naturally
    if random.random() < 0.12:
        hotspot_score = random.randint(80,100)
    elif random.random() < 0.35:
        hotspot_score = random.randint(55,79)
    else:
        hotspot_score = random.randint(5,54)


    crime_category, crime_type = get_random_crime()

    severity = get_crime_severity(crime_category)

    fir_status = get_fir_status(severity)

    response_time = get_response_time(severity)

    time_slot = get_time_slot(crime_type)

    cctv_available = get_cctv_availability(crime_type)


# 40% chance of selecting a repeat offender
    if random.random() < 0.40:
        accused_id = random.choice(OFFENDERS)
    else:
        accused_id = f"ACC{random.randint(501,999999):06d}"

    crime = {
        "crime_id": f"CR{i + 1:06d}",
        "crime_datetime": fake.date_time_between(
        start_date="-2y",
        end_date="now"
        ).strftime("%Y-%m-%d %H:%M:%S"),
        "time_slot": time_slot,
        "district_id": location["district_id"],
        "district": location["district_name"],

        "taluk_id": location["taluk_id"],
        "taluk": location["taluk_name"],

        "gp_id": location["gp_id"],
        "gram_panchayat": (
            location["gp_name"]
            if not str(location["gp_name"]) == "nan"
            else "Unknown"
        ),

        "village_id": location["village_id"],
        "village": location["village_name"],
        "police_station_name": location["police_station_name"],
        

        "crime_latitude": round(
            location["latitude"] + random.uniform(-0.002,0.002),
            6
        ),

        "crime_longitude": round(
            location["longitude"] + random.uniform(-0.002,0.002),
            6
        ),
        "crime_category": crime_category,
        "crime_type": crime_type,
        "crime_severity": severity,
        "hotspot_score": hotspot_score,
        "victim_age": random.randint(18, 80),
        "victim_gender": get_victim_gender(crime_category),
        "accused_id": accused_id,
        "accused_age": random.randint(18, 70),
        "accused_gender": random.choice(["Male", "Female"]),
        "fir_registered": fir_status,
        "case_status": random.choice([
            "Under Investigation",
            "Charge Sheet Filed",
            "Closed",
            "Pending Trial"
        ]),
        "cctv_available": cctv_available,
        "response_time_minutes": response_time,
    }

    crime_records.append(crime)

df = pd.DataFrame(crime_records)

district_spread = (
    df.groupby("district")
      .agg(
          villages_used=("village_id", "nunique"),
          total_crimes=("crime_id", "count"),
      )
)

district_spread["avg_crimes_per_village"] = (
    district_spread["total_crimes"]
    / district_spread["villages_used"]
).round(2)

print("\nDistrict Spread:")
print(district_spread.sort_values("avg_crimes_per_village", ascending=False))

output_path = BASE_DIR / "datasets" / "raw" / "crime_cases.csv"

df.to_csv(output_path, index=False)

print(f"\nGenerated {len(df)} crime records.")
print(f"Saved to: {output_path}")

