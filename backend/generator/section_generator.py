from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]

OUTPUT_FILE = (
    BASE_DIR
    / "datasets"
    / "masters"
    / "section_master.csv"
)

sections = [
    {
        "section_id": "SEC001",
        "act_id": "ACT001",
        "section": "103",
        "offence": "Murder",
    },
    {
        "section_id": "SEC002",
        "act_id": "ACT001",
        "section": "109",
        "offence": "Attempt to Murder",
    },
    {
        "section_id": "SEC003",
        "act_id": "ACT001",
        "section": "303",
        "offence": "Theft",
    },
    {
        "section_id": "SEC004",
        "act_id": "ACT001",
        "section": "309",
        "offence": "Robbery",
    },
    {
        "section_id": "SEC005",
        "act_id": "ACT001",
        "section": "318",
        "offence": "Cheating",
    },
    {
        "section_id": "SEC006",
        "act_id": "ACT001",
        "section": "74",
        "offence": "Assault",
    },
    {
        "section_id": "SEC007",
        "act_id": "ACT001",
        "section": "75",
        "offence": "Sexual Harassment",
    },
    {
        "section_id": "SEC008",
        "act_id": "ACT002",
        "section": "66C",
        "offence": "Identity Theft",
    },
    {
        "section_id": "SEC009",
        "act_id": "ACT002",
        "section": "66D",
        "offence": "Online Cheating",
    },
    {
        "section_id": "SEC010",
        "act_id": "ACT004",
        "section": "21",
        "offence": "Illegal Drugs",
    },
    {
        "section_id": "SEC011",
        "act_id": "ACT006",
        "section": "25",
        "offence": "Illegal Arms",
    },

        {
        "section_id": "SEC012",
        "act_id": "ACT001",
        "section": "SYN001",
        "offence": "Domestic Violence",
    },
    {
        "section_id": "SEC013",
        "act_id": "ACT001",
        "section": "SYN002",
        "offence": "Stalking",
    },
    {
        "section_id": "SEC014",
        "act_id": "ACT002",
        "section": "SYN003",
        "offence": "Financial Fraud",
    },
    {
        "section_id": "SEC015",
        "act_id": "ACT001",
        "section": "SYN004",
        "offence": "Forgery",
    },
    {
        "section_id": "SEC016",
        "act_id": "ACT007",
        "section": "SYN005",
        "offence": "Illegal Gambling",
    },
    {
        "section_id": "SEC017",
        "act_id": "ACT004",
        "section": "SYN006",
        "offence": "Illegal Liquor",
    },
    {
        "section_id": "SEC018",
        "act_id": "ACT001",
        "section": "SYN007",
        "offence": "Rioting",
    },
    {
        "section_id": "SEC019",
        "act_id": "ACT001",
        "section": "SYN008",
        "offence": "Cattle Theft",
    },
    {
        "section_id": "SEC020",
        "act_id": "ACT001",
        "section": "SYN009",
        "offence": "Crop Theft",
    },
    {
        "section_id": "SEC021",
        "act_id": "ACT001",
        "section": "SYN010",
        "offence": "Sand Mining",
    },
]

section_df = pd.DataFrame(sections)

section_df.to_csv(
    OUTPUT_FILE,
    index=False,
)

print(section_df)

print(f"\nGenerated {len(section_df)} Sections.")

print(f"Saved to {OUTPUT_FILE}")