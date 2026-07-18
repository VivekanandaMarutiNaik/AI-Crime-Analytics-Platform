import random
from pathlib import Path

import pandas as pd
from faker import Faker

fake = Faker("en_IN")

BASE_DIR = Path(__file__).resolve().parents[2]

MASTER = pd.read_csv(
    BASE_DIR / "datasets" / "processed" / "master_locations.csv"
)

POLICE = pd.read_csv(
    BASE_DIR / "datasets" / "processed" / "police_master.csv"
)

print("Master Locations :", len(MASTER))
print("Police Stations  :", len(POLICE))