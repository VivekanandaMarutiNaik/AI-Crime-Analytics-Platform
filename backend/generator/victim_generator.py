import random

import pandas as pd
from faker import Faker

fake = Faker("en_IN")

# Load master datasets
CASE_MASTER = pd.read_csv("datasets/masters/case_master.csv")

print(f"Cases loaded: {len(CASE_MASTER)}")

# Store generated victim records
victims = []

# Generate Victim ID
def generate_victim_id(index):
    return f"VICT{index:06d}"

for _, case in CASE_MASTER.iterrows():
    case_id = case["case_id"]

    # Decide how many victims this case has
    victim_count = random.choices(
        [1, 2, 3],
        weights=[80, 15, 5],
        k=1
    )[0]

    for _ in range(victim_count):
        victim_id = generate_victim_id(len(victims) + 1)

        # Basic details
        gender = random.choice(["Male", "Female", "Other"])
        age = random.randint(1, 90)

        # Generate name based on gender
        if gender == "Male":
            victim_name = fake.name_male()
        elif gender == "Female":
            victim_name = fake.name_female()
        else:
            victim_name = fake.name()

        occupation = random.choice([
            "Student",
            "Farmer",
            "Business",
            "Government Employee",
            "Private Employee",
            "Labourer",
            "Driver",
            "Housewife",
            "Retired",
            "Self Employed",
            "Unemployed"
        ])

        injury_type = random.choices(
            ["None", "Minor", "Serious", "Fatal"],
            weights=[35, 40, 20, 5],
            k=1
        )[0]

        relationship_to_accused = random.choice([
            "Stranger",
            "Family",
            "Friend",
            "Neighbour",
            "Colleague",
            "Unknown"
        ])

        address = fake.address().replace("\n", ", ")

        # Add victim record
        victims.append({
            "victim_id": victim_id,
            "case_id": case_id,
            "victim_name": victim_name,
            "gender": gender,
            "age": age,
            "occupation": occupation,
            "injury_type": injury_type,
            "relationship_to_accused": relationship_to_accused,
            "address": address
        })

# Create DataFrame
victim_df = pd.DataFrame(victims)

# Save to CSV
output_path = "datasets/masters/victim_master.csv"
victim_df.to_csv(output_path, index=False)

print(f"Generated {len(victim_df)} victim records.")
print(f"Saved to: {output_path}")