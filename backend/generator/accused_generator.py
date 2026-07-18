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
    / "accused_master.csv"
)

cases = pd.read_csv(CASE_FILE)

accused = []

occupations = [
    "Farmer",
    "Business",
    "Driver",
    "Labourer",
    "Student",
    "Private Employee",
    "Government Employee",
    "Mechanic",
    "Electrician",
    "Self Employed",
]

for i, case in cases.iterrows():

    gender = random.choice(["Male", "Female"])

    accused.append({

        "accused_person_id": f"A{i+1:06d}",

        "case_id": case["case_id"],

        "accused_name": (
            fake.name_male()
            if gender == "Male"
            else fake.name_female()
        ),

        "gender": gender,

        "age": random.randint(18, 70),

        "occupation": random.choice(occupations),

        "is_arrested": random.choices(
            [True, False],
            weights=[80,20],
            k=1
        )[0],

        "is_history_sheeter": random.choices(
            [True, False],
            weights=[10,90],
            k=1
        )[0],

        "address": fake.address().replace("\n", ", "),
    })

accused_df = pd.DataFrame(accused)

accused_df.to_csv(
    OUTPUT_FILE,
    index=False,
)

print(accused_df.head())

print(f"\nGenerated {len(accused_df)} accused.")