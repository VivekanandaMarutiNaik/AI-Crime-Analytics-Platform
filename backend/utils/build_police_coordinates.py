from pathlib import Path
import pandas as pd
import time
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = BASE_DIR / "datasets" / "processed" / "police_master.csv"
OUTPUT_FILE = BASE_DIR / "datasets" / "processed" / "police_master_geocoded.csv"

# If we've already geocoded some stations, continue from there.
if OUTPUT_FILE.exists():
    df = pd.read_csv(OUTPUT_FILE)
    print(f"Resuming from {OUTPUT_FILE}")
else:
    df = pd.read_csv(INPUT_FILE)
    print(f"Starting from {INPUT_FILE}")

# Create tracking columns only once
if "geocode_status" not in df.columns:
    df["geocode_status"] = ""

if "geocode_query" not in df.columns:
    df["geocode_query"] = ""

print(f"Total stations: {len(df)}")

geolocator = Nominatim(user_agent="karnataka_police_geocoder_v2")
geocode = RateLimiter(
    geolocator.geocode,
    min_delay_seconds=1.2,
    swallow_exceptions=True,
)

MIN_LAT = 11.3
MAX_LAT = 18.7
MIN_LON = 73.8
MAX_LON = 78.9


def inside_karnataka(lat, lon):
    return (
        MIN_LAT <= lat <= MAX_LAT
        and MIN_LON <= lon <= MAX_LON
    )


TEST_MODE = True
MAX_TEST = 10

processed = 0

for index, row in df.iterrows():

    if TEST_MODE and processed >= MAX_TEST:
        break

    # Skip stations already geocoded successfully
    if str(row["geocode_status"]).strip() == "AUTO":
        continue

    queries = [
        f"{row['police_station_name']}, {row['address']}, {row['ksp_district']}, Karnataka, India",
        f"{row['police_station_name']}, {row['circle']}, {row['ksp_district']}, Karnataka, India",
        f"{row['police_station_name']}, {row['ksp_district']}, Karnataka, India",
        f"{row['police_station_name']}, Karnataka, India",
    ]

    found = False

    for query in queries:

        location = geocode(query)

        if (
            location
            and inside_karnataka(location.latitude, location.longitude)
        ):
            df.at[index, "latitude"] = round(location.latitude, 6)
            df.at[index, "longitude"] = round(location.longitude, 6)
            df.at[index, "geocode_status"] = "AUTO"
            df.at[index, "geocode_query"] = query

            print(f"✓ {index + 1}/{len(df)}  {row['police_station_name']}")

            # Save after every successful geocode
            df.to_csv(OUTPUT_FILE, index=False)

            processed += 1
            found = True
            break

    if not found:
        df.at[index, "geocode_status"] = "MANUAL"
        df.at[index, "geocode_query"] = "NOT_FOUND"

        print(f"✗ {index + 1}/{len(df)}  {row['police_station_name']}")

        df.to_csv(OUTPUT_FILE, index=False)

        processed += 1

    time.sleep(0.2)

print("\nFinished!")