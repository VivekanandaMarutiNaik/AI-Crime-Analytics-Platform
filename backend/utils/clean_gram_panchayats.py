import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

gp_file = BASE_DIR / "datasets" / "official" / "gram_panchayats.xlsx"
mapping_file = BASE_DIR / "datasets" / "official" / "gp_village_mapping.xlsx"
output_file = BASE_DIR / "datasets" / "raw" / "gram_panchayats.csv"

# -------------------------
# Read Gram Panchayat file
# -------------------------
gp = pd.read_excel(
    gp_file,
    header=3,
    skiprows=[4],
    engine="openpyxl"
)

gp.columns = gp.columns.str.strip()

gp = gp[
    [
        "Localbody Code",
        "Localbody Name"
    ]
]

gp.columns = [
    "gp_id",
    "gp_name"
]

gp = gp.dropna(subset=["gp_id"])
gp["gp_id"] = gp["gp_id"].astype(int)
gp["gp_name"] = gp["gp_name"].astype(str).str.strip()

# -------------------------
# Read Mapping file
# -------------------------
mapping = pd.read_excel(
    mapping_file,
    header=4,
    skiprows=[5],
    engine="openpyxl"
)

mapping.columns = mapping.columns.str.strip()

mapping = mapping[
    [
        "Village Code",
        "Local Body Code"
    ]
]

mapping.columns = [
    "village_id",
    "gp_id"
]

mapping = mapping.dropna()

mapping["village_id"] = mapping["village_id"].astype(int)
mapping["gp_id"] = mapping["gp_id"].astype(int)

# -------------------------
# Merge GP names
# -------------------------
result = mapping.merge(
    gp,
    on="gp_id",
    how="left"
)

# Keep only one GP per village
result = (
    result
    .sort_values(["village_id", "gp_id"])
    .drop_duplicates(subset=["village_id"], keep="first")
)

result.to_csv(output_file, index=False)

print(result.head())

print(f"\nVillage-GP mappings : {len(result)}")
print(f"Unique Gram Panchayats : {result['gp_id'].nunique()}")
print(f"Saved to : {output_file}")