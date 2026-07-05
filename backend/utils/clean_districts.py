import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

official_file = BASE_DIR / "datasets" / "official" / "districts.xlsx"
output_file = BASE_DIR / "datasets" / "raw" / "districts.csv"

# Read the LGD file
df = pd.read_excel(
    official_file,
    header=3,
    skiprows=[4],
    engine="openpyxl"
)

# Keep only required columns
df = df[
    [
        "District Code",
        "District Name"
    ]
]

# Rename columns
df.columns = [
    "district_id",
    "district_name"
]

# Remove blank rows
df = df.dropna(subset=["district_id"])

# Convert IDs to integers
df["district_id"] = df["district_id"].astype(int)

# Sort
df = df.sort_values("district_name")

# Save
df.to_csv(output_file, index=False)

print(df.head())

print(f"\nTotal Districts : {len(df)}")
print(f"Saved to : {output_file}")