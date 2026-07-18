import pandas as pd

# Load complainant master
COMPLAINANT_MASTER = pd.read_csv("datasets/masters/complainant_master.csv")

print(f"Complainants loaded: {len(COMPLAINANT_MASTER)}")

# Collect unique religions
religions = sorted(COMPLAINANT_MASTER["religion"].dropna().unique())

print(f"Unique religions found: {len(religions)}")
print(religions)

# Create religion master
religion_master = pd.DataFrame({
    "religion_id": [
        f"REL{str(i + 1).zfill(3)}"
        for i in range(len(religions))
    ],
    "religion_name": religions
})

print(religion_master)

# Save religion master
output_path = "datasets/masters/religion_master.csv"
religion_master.to_csv(output_path, index=False)

print(f"\nGenerated {len(religion_master)} religion records.")
print(f"Saved to: {output_path}")