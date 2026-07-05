import random
from pathlib import Path

import pandas as pd
from faker import Faker

fake = Faker("en_IN")

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

CRIME_CATEGORIES = {
    "Property Crime": [
        "Vehicle Theft",
        "House Burglary",
        "Chain Snatching",
        "Shop Theft"
    ],
    "Violent Crime": [
        "Assault",
        "Robbery",
        "Murder",
        "Attempt to Murder"
    ],
    "Crime Against Women": [
        "Domestic Violence",
        "Sexual Harassment",
        "Stalking"
    ],
    "Cyber Crime": [
        "UPI Fraud",
        "Phishing",
        "OTP Scam"
    ],
    "Economic Crime": [
        "Cheating",
        "Forgery",
        "Financial Fraud"
    ],
    "Public Order": [
        "Rioting",
        "Illegal Gambling",
        "Illegal Liquor"
    ],
    "Rural Crime": [
        "Crop Theft",
        "Cattle Theft",
        "Sand Mining"
    ]
}
# Pick one random location
location = MASTER_LOCATIONS.sample(1).iloc[0]


print("\nRandom Location:")
print(location)

# Select a random crime category
crime_category = random.choice(list(CRIME_CATEGORIES.keys()))

# Select a random crime type from that category
crime_type = random.choice(CRIME_CATEGORIES[crime_category])

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
    "gram_panchayat": location["gp_name"],
    "crime_category": crime_category,
    "crime_type": crime_type,
    "victim_age": random.randint(18, 80),
    "victim_gender": random.choice(["Male", "Female"]),
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