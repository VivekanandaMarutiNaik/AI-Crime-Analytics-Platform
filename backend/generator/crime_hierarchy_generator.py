import pandas as pd
# Load master datasets
CASE_MASTER = pd.read_csv("datasets/masters/case_master.csv")
ACT_MASTER = pd.read_csv("datasets/masters/act_master.csv")
SECTION_MASTER = pd.read_csv("datasets/masters/section_master.csv")
CRIME_LAW_MAPPING = pd.read_csv("datasets/masters/crime_law_mapping.csv")

print(f"Cases loaded: {len(CASE_MASTER)}")
print(f"Acts loaded: {len(ACT_MASTER)}")
print(f"Sections loaded: {len(SECTION_MASTER)}")
print(f"Crime-law mappings loaded: {len(CRIME_LAW_MAPPING)}")

# Extract unique Crime Head (crime_category)
crime_heads = sorted(CASE_MASTER["crime_category"].dropna().unique())

# Extract unique Crime Head → Crime Sub Head pairs
crime_subheads = (
    CASE_MASTER[["crime_category", "crime_type"]]
    .drop_duplicates()
    .sort_values(["crime_category", "crime_type"])
    .reset_index(drop=True)
)

print(f"Crime Heads found: {len(crime_heads)}")
print(f"Crime Sub Heads found: {len(crime_subheads)}")

print("\nCrime Heads:")
print(crime_heads)

print("\nCrime Head -> Crime Sub Head Mapping:")
print(crime_subheads.head(20))

# Create Crime Head Master
crime_head_master = pd.DataFrame({
    "crime_head_id": [
        f"CH{str(i + 1).zfill(3)}"
        for i in range(len(crime_heads))
    ],
    "crime_head_name": crime_heads
})

print("\nCrime Head Master")
print(crime_head_master)

# Create lookup from Crime Head name -> Crime Head ID
crime_head_lookup = dict(
    zip(
        crime_head_master["crime_head_name"],
        crime_head_master["crime_head_id"]
    )
)

crime_subhead_records = []

for i, row in crime_subheads.iterrows():
    crime_subhead_records.append({
        "crime_subhead_id": f"CSH{str(i + 1).zfill(3)}",
        "crime_head_id": crime_head_lookup[row["crime_category"]],
        "crime_subhead_name": row["crime_type"]
    })

crime_subhead_master = pd.DataFrame(crime_subhead_records)

print("\nCrime Sub Head Master")
print(crime_subhead_master)