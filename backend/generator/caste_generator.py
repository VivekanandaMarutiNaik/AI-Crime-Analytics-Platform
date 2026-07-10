import pandas as pd

# Load complainant master
COMPLAINANT_MASTER = pd.read_csv("datasets/masters/complainant_master.csv")

print(f"Complainants loaded: {len(COMPLAINANT_MASTER)}")

# Collect unique castes
castes = sorted(COMPLAINANT_MASTER["caste"].dropna().unique())

print(f"Unique castes found: {len(castes)}")
print(castes)

# Create caste master
caste_master = pd.DataFrame({
    "caste_id": [
        f"CAS{str(i + 1).zfill(3)}"
        for i in range(len(castes))
    ],
    "caste_name": castes
})

print(caste_master)

# Save caste master
output_path = "datasets/masters/caste_master.csv"
caste_master.to_csv(output_path, index=False)

print(f"\nGenerated {len(caste_master)} caste records.")
print(f"Saved to: {output_path}")