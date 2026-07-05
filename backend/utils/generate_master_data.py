import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

RAW_DATA = BASE_DIR / "datasets" / "raw"

RAW_DATA.mkdir(parents=True, exist_ok=True)

districts = [
    "Bagalkot",
    "Ballari",
    "Belagavi",
    "Bengaluru Rural",
    "Bengaluru Urban",
    "Bidar",
    "Chamarajanagar",
    "Chikkaballapur",
    "Chikkamagaluru",
    "Chitradurga",
    "Dakshina Kannada",
    "Davanagere",
    "Dharwad",
    "Gadag",
    "Hassan",
    "Haveri",
    "Kalaburagi",
    "Kodagu",
    "Kolar",
    "Koppal",
    "Mandya",
    "Mysuru",
    "Raichur",
    "Ramanagara",
    "Shivamogga",
    "Tumakuru",
    "Udupi",
    "Uttara Kannada",
    "Vijayapura",
    "Yadgir",
    "Vijayanagara"
]

districts_df = pd.DataFrame({
    "district_id": range(1, len(districts) + 1),
    "district_name": districts
})

districts_df.to_csv(
    RAW_DATA / "districts.csv",
    index=False
)

print("✅ districts.csv generated successfully!")

# Sample taluks (We'll expand this later)

taluks = [
    (1, "Badami"),
    (1, "Hungund"),
    (1, "Mudhol"),

    (2, "Ballari"),
    (2, "Hospet"),
    (2, "Siruguppa"),

    (3, "Belagavi"),
    (3, "Gokak"),
    (3, "Athani"),

    (4, "Devanahalli"),
    (4, "Doddaballapur"),

    (5, "Bengaluru North"),
    (5, "Bengaluru South"),
    (5, "Yelahanka")
]

taluks_df = pd.DataFrame({
    "taluk_id": range(1, len(taluks)+1),
    "district_id": [x[0] for x in taluks],
    "taluk_name": [x[1] for x in taluks]
})

taluks_df.to_csv(
    RAW_DATA / "taluks.csv",
    index=False
)

print("✅ taluks.csv generated successfully!")

# Sample Gram Panchayats

gram_panchayats = [
    (1, "Kerur"),
    (1, "Kataraki"),
    (2, "Amingad"),
    (2, "Ilkal Rural"),
    (3, "Lokapur"),
    (4, "Kudatini"),
    (5, "Kamalapura"),
    (6, "Tekkalakote"),
    (7, "Kakati"),
    (8, "Gokak Rural"),
    (9, "Athani Rural"),
    (10, "Vijayapura"),
    (11, "Kodigehalli"),
    (12, "Yelahanka"),
    (13, "JP Nagar"),
    (14, "Begur")
]

gram_panchayats_df = pd.DataFrame({
    "gp_id": range(1, len(gram_panchayats) + 1),
    "taluk_id": [x[0] for x in gram_panchayats],
    "gp_name": [x[1] for x in gram_panchayats]
})

gram_panchayats_df.to_csv(
    RAW_DATA / "gram_panchayats.csv",
    index=False
)

print("✅ gram_panchayats.csv generated successfully!")

# Sample Police Stations

police_stations = [
    (1, 1, "Badami Police Station", "Rural", 15.9149, 75.6766),
    (1, 2, "Hungund Police Station", "Rural", 16.0620, 76.0580),
    (1, 3, "Mudhol Police Station", "Urban", 16.3333, 75.2833),

    (2, 4, "Ballari Police Station", "Urban", 15.1394, 76.9214),
    (2, 5, "Hospet Police Station", "Urban", 15.2695, 76.3871),
    (2, 6, "Siruguppa Police Station", "Rural", 15.6333, 76.9000),

    (3, 7, "Belagavi Police Station", "Urban", 15.8497, 74.4977),
    (3, 8, "Gokak Police Station", "Urban", 16.1667, 74.8333),
    (3, 9, "Athani Police Station", "Rural", 16.7269, 75.0643),

    (4, 10, "Devanahalli Police Station", "Urban", 13.2422, 77.7132),

    (5, 11, "Bengaluru North Police Station", "Urban", 13.0827, 77.5877),
    (5, 12, "Bengaluru South Police Station", "Urban", 12.9716, 77.5946),
    (5, 13, "Yelahanka Police Station", "Urban", 13.1005, 77.5963)
]

police_stations_df = pd.DataFrame({
    "station_id": range(1, len(police_stations) + 1),
    "district_id": [x[0] for x in police_stations],
    "taluk_id": [x[1] for x in police_stations],
    "station_name": [x[2] for x in police_stations],
    "station_type": [x[3] for x in police_stations],
    "latitude": [x[4] for x in police_stations],
    "longitude": [x[5] for x in police_stations]
})

police_stations_df.to_csv(
    RAW_DATA / "police_stations.csv",
    index=False
)

print("✅ police_stations.csv generated successfully!")