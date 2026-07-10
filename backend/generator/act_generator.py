from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]

OUTPUT_FILE = (
    BASE_DIR
    / "datasets"
    / "masters"
    / "act_master.csv"
)

acts = [
    {
        "act_id": "ACT001",
        "act_name": "Bharatiya Nyaya Sanhita, 2023",
        "short_name": "BNS",
    },
    {
        "act_id": "ACT002",
        "act_name": "Information Technology Act, 2000",
        "short_name": "IT Act",
    },
    {
        "act_id": "ACT003",
        "act_name": "Protection of Children from Sexual Offences Act, 2012",
        "short_name": "POCSO",
    },
    {
        "act_id": "ACT004",
        "act_name": "Narcotic Drugs and Psychotropic Substances Act",
        "short_name": "NDPS",
    },
    {
        "act_id": "ACT005",
        "act_name": "Motor Vehicles Act",
        "short_name": "MV Act",
    },
    {
        "act_id": "ACT006",
        "act_name": "Arms Act",
        "short_name": "Arms Act",
    },
    {
        "act_id": "ACT007",
        "act_name": "Karnataka Police Act",
        "short_name": "KP Act",
    },
]

act_df = pd.DataFrame(acts)

act_df.to_csv(
    OUTPUT_FILE,
    index=False,
)

print(act_df)

print(f"\nGenerated {len(act_df)} Acts.")

print(f"Saved to {OUTPUT_FILE}")