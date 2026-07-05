import random
from pathlib import Path
from rules import (
    get_random_crime,
    get_victim_gender,
    get_random_police_station,
)

import pandas as pd
from faker import Faker

fake = Faker("en_IN")
NUM_RECORDS = 10

from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[2]

MASTER_LOCATIONS = pd.read_csv(
    BASE_DIR / "datasets" / "processed" / "master_locations.csv"
)

POLICE_STATIONS = pd.read_csv(
    BASE_DIR / "datasets" / "raw" / "police_stations.csv"
)

print(f"Master Locations : {len(MASTER_LOCATIONS)}")
print(f"Police Stations  : {len(POLICE_STATIONS)}")


for i in range(NUM_RECORDS):

    # Pick one random location
    location = MASTER_LOCATIONS.sample(1).iloc[0]


    print("\nRandom Location:")
    print(location)

    crime_category, crime_type = get_random_crime()

    police_station = get_random_police_station(POLICE_STATIONS)

    print("\nCrime Details:")
    print(f"Category : {crime_category}")
    print(f"Type     : {crime_type}")

    crime = {
        "crime_id": f"CR{random.randint(1, 999999):06d}",
        "crime_datetime": fake.date_time_between(
        start_date="-2y",
        end_date="now"
        ).strftime("%Y-%m-%d %H:%M:%S"),
        "district": location["district_name"],
        "taluk": location["taluk_name"],
        "village": location["village_name"],
        "gram_panchayat": (
            location["gp_name"]
            if not str(location["gp_name"]) == "nan"
            else "Unknown"
        ),
        "police_station_id": police_station["station_id"],
        "police_station_name": police_station["station_name"],
        "crime_category": crime_category,
        "crime_type": crime_type,
        "victim_age": random.randint(18, 80),
        "victim_gender": get_victim_gender(crime_category),
        "accused_age": random.randint(18, 70),
        "accused_gender": random.choice(["Male", "Female"]),
        "fir_registered": random.choice(["Yes", "No"]),
        "case_status": random.choice([
            "Under Investigation",
            "Charge Sheet Filed",
            "Closed",
            "Pending Trial"
        ]),
        "cctv_available": random.choice(["Yes", "No"]),
        "response_time_minutes": random.randint(5, 120),
    }

    print("\nGenerated Crime Record:")
    print(crime)