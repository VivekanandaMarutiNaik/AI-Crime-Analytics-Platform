import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

official_file = BASE_DIR / "datasets" / "official" / "villages.xlsx"
output_file = BASE_DIR / "datasets" / "raw" / "villages.csv"

# Read LGD file
df = pd.read_excel(
    official_file,
    header=3,
    skiprows=[4],
    engine="openpyxl"
)

# Select columns by index (avoids duplicate column name issues)
df = df.iloc[:, [5, 7, 3, 4, 1, 2]]

# Rename columns
df.columns = [
    "village_id",
    "village_name",
    "taluk_id",
    "taluk_name",
    "district_id",
    "district_name"
]

# Remove blank rows
df = df.dropna(subset=["village_id"])

# Convert IDs
df["village_id"] = df["village_id"].astype(int)
df["taluk_id"] = df["taluk_id"].astype(int)
df["district_id"] = df["district_id"].astype(int)

# Clean text
for col in ["village_name", "taluk_name", "district_name"]:
    df[col] = df[col].astype(str).str.strip()

# Remove duplicates
df = df.drop_duplicates(subset=["village_id"])

# Sort
df = df.sort_values(
    ["district_name", "taluk_name", "village_name"]
)

# Save
df.to_csv(output_file, index=False)

print(df.head())
print(f"\nTotal Villages : {len(df)}")
print(f"Saved to : {output_file}")