import random
from pathlib import Path
from rules import (
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
NUM_RECORDS = 10000

from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[2]

LOCATION_MASTER = pd.read_csv(
    BASE_DIR / "datasets" / "processed" / "police_village_mapping.csv"
)

# Select hotspot villages (about 5% of all villages)
HOTSPOT_VILLAGES = set(
    LOCATION_MASTER.sample(frac=0.05)["village_id"]
)

HOTSPOT_SCORES = {}

for village_id in HOTSPOT_VILLAGES:
    HOTSPOT_SCORES[village_id] = random.randint(70, 100)


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
    if random.random() < 0.70:
        hotspot_locations = LOCATION_MASTER[
        LOCATION_MASTER["village_id"].isin(HOTSPOT_VILLAGES)
    ]
        location = hotspot_locations.sample(1).iloc[0]
    else:
        location = LOCATION_MASTER.sample(1).iloc[0]
    
    hotspot_score = HOTSPOT_SCORES.get(
        location["village_id"],
        random.randint(0, 30)
    )


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
        "police_station_latitude": location["police_station_latitude"],
        "police_station_longitude": location["police_station_longitude"],

        "crime_latitude": round(
            location["police_station_latitude"] + random.uniform(-0.003, 0.003),
            6
        ),

        "crime_longitude": round(
            location["police_station_longitude"] + random.uniform(-0.003, 0.003),
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

output_path = BASE_DIR / "datasets" / "raw" / "crime_cases.csv"

df.to_csv(output_path, index=False)

print(f"\nGenerated {len(df)} crime records.")
print(f"Saved to: {output_path}")

