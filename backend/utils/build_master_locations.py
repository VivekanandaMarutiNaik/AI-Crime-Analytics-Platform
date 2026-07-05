import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

RAW = BASE_DIR / "datasets" / "raw"
PROCESSED = BASE_DIR / "datasets" / "processed"

# Load cleaned datasets
districts = pd.read_csv(RAW / "districts.csv")
taluks = pd.read_csv(RAW / "taluks.csv")
villages = pd.read_csv(RAW / "villages.csv")
gps = pd.read_csv(RAW / "gram_panchayats.csv")

# Merge villages with GP mapping
master = villages.merge(
    gps,
    on="village_id",
    how="left"
)

# Create processed folder if it doesn't exist
PROCESSED.mkdir(parents=True, exist_ok=True)

# Save
output_file = PROCESSED / "master_locations.csv"
master.to_csv(output_file, index=False)

print(master.head())

print("\nRows:", len(master))
print("Columns:", list(master.columns))
print(f"\nSaved to: {output_file}")