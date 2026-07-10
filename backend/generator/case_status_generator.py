import pandas as pd

# Load case master
CASE_MASTER = pd.read_csv("datasets/masters/case_master.csv")

print(f"Cases loaded: {len(CASE_MASTER)}")

# Collect unique case statuses
case_statuses = sorted(CASE_MASTER["case_status"].dropna().unique())

print(f"Unique case statuses found: {len(case_statuses)}")
print(case_statuses)

# Create case status master
case_status_master = pd.DataFrame({
    "case_status_id": [
        f"CS{str(i + 1).zfill(3)}"
        for i in range(len(case_statuses))
    ],
    "case_status_name": case_statuses
})

print(case_status_master)

# Save case status master
output_path = "datasets/masters/case_status_master.csv"
case_status_master.to_csv(output_path, index=False)

print(f"\nGenerated {len(case_status_master)} case status records.")
print(f"Saved to: {output_path}")