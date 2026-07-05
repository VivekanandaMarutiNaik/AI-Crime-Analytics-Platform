import random
import pandas as pd
from faker import Faker
from pathlib import Path

fake = Faker("en_IN")

BASE_DIR = Path(__file__).resolve().parents[2]

MASTER_FILE = (
    BASE_DIR /
    "datasets" /
    "processed" /
    "master_locations.csv"
)

master = pd.read_csv(MASTER_FILE)

print(master.head())
print(f"\nTotal locations: {len(master)}")
crime_categories = {
    "Theft": [
        "Mobile Theft",
        "Vehicle Theft",
        "House Burglary"
    ],
    "Violent Crime": [
        "Assault",
        "Robbery",
        "Murder"
    ],
    "Cyber Crime": [
        "UPI Fraud",
        "Phishing",
        "Identity Theft"
    ],
    "Women Safety": [
        "Harassment",
        "Domestic Violence",
        "Stalking"
    ]
}

location = master.sample(1).iloc[0]

category = random.choice(list(crime_categories.keys()))
crime = random.choice(crime_categories[category])

record = {
    "crime_id": "CR000001",
    "category": category,
    "crime_type": crime,
    "district": location["district_name"],
    "taluk": location["taluk_name"],
    "gram_panchayat": location["gp_name"],
    "police_station": location["station_name"],
    "victim_name": fake.name(),
    "status": "Open"
}

print(record)