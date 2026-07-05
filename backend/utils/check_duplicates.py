import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

gps = pd.read_csv(BASE_DIR / "datasets" / "raw" / "gram_panchayats.csv")

duplicates = gps[gps.duplicated(subset=["village_id"], keep=False)]

print(f"Duplicate village IDs: {duplicates['village_id'].nunique()}")
print()
print(duplicates.sort_values("village_id"))