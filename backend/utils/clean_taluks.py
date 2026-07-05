import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

official_file = BASE_DIR / "datasets" / "official" / "subdistricts.xlsx"
output_file = BASE_DIR / "datasets" / "raw" / "taluks.csv"

# Read LGD file
df = pd.read_excel(
    official_file,
    header=3,
    skiprows=[4],
    engine="openpyxl"
)

# Keep only required columns
df = df[
    [
        "Subdistrict Code",
        "Subdistrict Name  ",
        "District code",
        "District Name"
    ]
]

# Rename columns
df.columns = [
    "taluk_id",
    "taluk_name",
    "district_id",
    "district_name"
]

# Remove blank rows
df = df.dropna(subset=["taluk_id"])

# Convert IDs
df["taluk_id"] = df["taluk_id"].astype(int)
df["district_id"] = df["district_id"].astype(int)

# Clean names
df["taluk_name"] = df["taluk_name"].astype(str).str.strip()
df["district_name"] = df["district_name"].astype(str).str.strip()

# Remove duplicates if any
df = df.drop_duplicates(subset=["taluk_id"])

# Sort
df = df.sort_values(["district_name", "taluk_name"])

# Save
df.to_csv(output_file, index=False)

print(df.head())

print(f"\nTotal Taluks : {len(df)}")
print(f"Saved to : {output_file}")