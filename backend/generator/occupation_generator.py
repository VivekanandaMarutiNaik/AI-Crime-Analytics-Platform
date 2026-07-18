import pandas as pd

# Load master datasets
COMPLAINANT_MASTER = pd.read_csv("datasets/masters/complainant_master.csv")
ACCUSED_MASTER = pd.read_csv("datasets/masters/accused_master.csv")
VICTIM_MASTER = pd.read_csv("datasets/masters/victim_master.csv")

print(f"Complainants loaded: {len(COMPLAINANT_MASTER)}")
print(f"Accused loaded: {len(ACCUSED_MASTER)}")
print(f"Victims loaded: {len(VICTIM_MASTER)}")

# Collect occupations from all master tables
occupations = set()

occupations.update(COMPLAINANT_MASTER["occupation"].dropna().unique())
occupations.update(ACCUSED_MASTER["occupation"].dropna().unique())
occupations.update(VICTIM_MASTER["occupation"].dropna().unique())

# Sort alphabetically
occupations = sorted(occupations)

print(f"Unique occupations found: {len(occupations)}")

# Create occupation master
occupation_master = pd.DataFrame({
    "occupation_id": [
        f"OCC{str(i + 1).zfill(3)}"
        for i in range(len(occupations))
    ],
    "occupation_name": occupations
})

print(occupation_master)

# Save occupation master
output_path = "datasets/masters/occupation_master.csv"
occupation_master.to_csv(output_path, index=False)

print(f"\nGenerated {len(occupation_master)} occupation records.")
print(f"Saved to: {output_path}")