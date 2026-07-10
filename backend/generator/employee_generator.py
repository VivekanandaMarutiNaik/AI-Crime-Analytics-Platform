import random
from pathlib import Path

import pandas as pd
from faker import Faker

fake = Faker("en_IN")

BASE_DIR = Path(__file__).resolve().parents[2]

POLICE_FILE = (
    BASE_DIR
    / "datasets"
    / "raw"
    / "crime_cases.csv"
)

OUTPUT_FILE = (
    BASE_DIR
    / "datasets"
    / "masters"
    / "employee_master.csv"
)

police = (
    pd.read_csv(POLICE_FILE)
    .sort_values("district")
    .drop_duplicates(subset=["police_station_name"])
    [
        [
            "district",
            "district_id",
            "taluk",
            "taluk_id",
            "police_station_name",
        ]
    ]
    .reset_index(drop=True)
)

print("Unique police stations:", len(police))

employees = []

RANKS = [
    ("Director General of Police", "DGP"),
    ("Additional Director General of Police", "ADGP"),
    ("Inspector General of Police", "IGP"),
    ("Deputy Inspector General of Police", "DIG"),
    ("Superintendent of Police", "SP"),
    ("Additional Superintendent of Police", "Addl. SP"),
    ("Deputy Superintendent of Police", "DySP"),
    ("Police Inspector", "PI"),
    ("Police Sub Inspector", "PSI"),
    ("Assistant Sub Inspector", "ASI"),
    ("Head Constable", "HC"),
    ("Police Constable", "PC"),
]

employee_id = 1

for _, station in police.iterrows():

    employee_count = random.randint(8, 18)

    for _ in range(employee_count):

        rank_name, rank_code = random.choices(
            RANKS,
            weights=[1, 2, 3, 4, 6, 8, 12, 18, 30, 45, 80, 220],
            k=1,
        )[0]

        employees.append({
            "employee_id": f"EMP{employee_id:06d}",
            "kgid": random.randint(100000, 999999),
            "employee_name": fake.name(),
            "gender": random.choice(["Male", "Female"]),
            "date_of_birth": fake.date_between(
                start_date="-58y",
                end_date="-22y",
            ),
            "blood_group": random.choice([
                "A+","A-","B+","B-","AB+","AB-","O+","O-"
            ]),
            "rank": rank_name,
            "rank_code": rank_code,
            "appointment_date": fake.date_between(
                start_date="-30y",
                end_date="-1y",
            ),
            "district": station["district"],
            "taluk": station["taluk"],
            "police_station_name": station["police_station_name"],
            "police_station_id": (
                station["police_station_name"]
                .upper()
                .replace(" ", "_")
            ),
        })

        employee_id += 1

employee_df = pd.DataFrame(employees)

employee_df.to_csv(
    OUTPUT_FILE,
    index=False,
)

print(employee_df.head())

print(f"\nGenerated {len(employee_df)} employees.")

print(f"Saved to {OUTPUT_FILE}")