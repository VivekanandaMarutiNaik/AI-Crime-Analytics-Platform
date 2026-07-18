import random
from pathlib import Path

import pandas as pd
from faker import Faker

fake = Faker("en_IN")

BASE_DIR = Path(__file__).resolve().parents[2]

CASE_FILE = (
    BASE_DIR
    / "datasets"
    / "masters"
    / "case_master.csv"
)

OUTPUT_FILE = (
    BASE_DIR
    / "datasets"
    / "masters"
    / "complainant_master.csv"
)

cases = pd.read_csv(CASE_FILE)

complainants = []

occupations = [
    "Farmer",
    "Business",
    "Government Employee",
    "Private Employee",
    "Student",
    "Homemaker",
    "Driver",
    "Labourer",
    "Retired",
    "Self Employed",
]

religions = [
    "Hindu",
    "Muslim",
    "Christian",
    "Jain",
    "Sikh",
]

castes = [
    "General",
    "OBC",
    "SC",
    "ST",
]

for i, case in cases.iterrows():

    gender = random.choice(["Male", "Female"])

    complainants.append({

        "complainant_id": f"CMP{i+1:06d}",

        "case_id": case["case_id"],

        "complainant_name": fake.name_male() if gender == "Male"
        else fake.name_female(),

        "gender": gender,

        "age": random.randint(18, 75),

        "occupation": random.choice(occupations),

        "religion": random.choice(religions),

        "caste": random.choice(castes),

        "mobile_number": fake.msisdn()[:10],

        "address": fake.address().replace("\n", ", "),

    })

complainant_df = pd.DataFrame(complainants)

complainant_df.to_csv(
    OUTPUT_FILE,
    index=False,
)

print(complainant_df.head())

print(f"\nGenerated {len(complainant_df)} complainants.")