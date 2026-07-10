from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]

OUTPUT_FILE = (
    BASE_DIR
    / "datasets"
    / "masters"
    / "crime_law_mapping.csv"
)

mapping = [
    {"crime_type":"Assault","act_id":"ACT001","section_id":"SEC006"},
    {"crime_type":"Domestic Violence","act_id":"ACT001","section_id":"SEC012"},
    {"crime_type":"Sexual Harassment","act_id":"ACT001","section_id":"SEC007"},
    {"crime_type":"Stalking","act_id":"ACT001","section_id":"SEC013"},

    {"crime_type":"OTP Scam","act_id":"ACT002","section_id":"SEC009"},
    {"crime_type":"Phishing","act_id":"ACT002","section_id":"SEC009"},
    {"crime_type":"UPI Fraud","act_id":"ACT002","section_id":"SEC008"},

    {"crime_type":"Cheating","act_id":"ACT001","section_id":"SEC005"},
    {"crime_type":"Financial Fraud","act_id":"ACT002","section_id":"SEC014"},
    {"crime_type":"Forgery","act_id":"ACT001","section_id":"SEC015"},

    {"crime_type":"Shop Theft","act_id":"ACT001","section_id":"SEC003"},
    {"crime_type":"House Burglary","act_id":"ACT001","section_id":"SEC003"},
    {"crime_type":"Vehicle Theft","act_id":"ACT001","section_id":"SEC003"},
    {"crime_type":"Chain Snatching","act_id":"ACT001","section_id":"SEC004"},

    {"crime_type":"Illegal Gambling","act_id":"ACT007","section_id":"SEC016"},
    {"crime_type":"Illegal Liquor","act_id":"ACT004","section_id":"SEC017"},
    {"crime_type":"Rioting","act_id":"ACT001","section_id":"SEC018"},

    {"crime_type":"Cattle Theft","act_id":"ACT001","section_id":"SEC019"},
    {"crime_type":"Crop Theft","act_id":"ACT001","section_id":"SEC020"},
    {"crime_type":"Sand Mining","act_id":"ACT001","section_id":"SEC021"},

    # Keep these because they exist in section_master and may be used later
    {"crime_type":"Murder","act_id":"ACT001","section_id":"SEC001"},
    {"crime_type":"Attempt to Murder","act_id":"ACT001","section_id":"SEC002"},
    {"crime_type":"Robbery","act_id":"ACT001","section_id":"SEC004"},
]

mapping_df = pd.DataFrame(mapping)

mapping_df.to_csv(
    OUTPUT_FILE,
    index=False,
)

print(mapping_df)

print(f"\nGenerated {len(mapping_df)} crime-law mappings.")