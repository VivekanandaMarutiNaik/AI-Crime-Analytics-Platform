import time
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

INPUT_FILE = "datasets/processed/police_master.csv"
OUTPUT_FILE = "datasets/processed/police_master_geocoded.csv"

df = pd.read_csv(INPUT_FILE)

geolocator = Nominatim(user_agent="karnataka_crime_dashboard_v1")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

MIN_LAT = 11.3
MAX_LAT = 18.7
MIN_LON = 73.8
MAX_LON = 78.9


def inside_karnataka(lat, lon):
    return (
        MIN_LAT <= lat <= MAX_LAT
        and MIN_LON <= lon <= MAX_LON
    )


new_lat = []
new_lon = []
status = []

for index, row in df.iterrows():
        # Keep existing valid coordinates
    if (
        pd.notna(row["latitude"])
        and pd.notna(row["longitude"])
        and inside_karnataka(row["latitude"], row["longitude"])
    ):
        new_lat.append(row["latitude"])
        new_lon.append(row["longitude"])
        status.append("EXISTING")
        continue

    queries = [
        f"{row['police_station_name']}, {row['address']}, {row['ksp_district']}, Karnataka, India",
        f"{row['police_station_name']}, {row['circle']}, {row['ksp_district']}, Karnataka, India",
        f"{row['police_station_name']}, {row['ksp_district']}, Karnataka, India",
        f"{row['police_station_name']}, {row['lgd_district']}, Karnataka, India",
    ]

    found = False

    for query in queries:

        try:
            location = geocode(query)

            if location:

                if inside_karnataka(location.latitude, location.longitude):

                    print(f"✓ {row['police_station_name']}")

                    new_lat.append(location.latitude)
                    new_lon.append(location.longitude)
                    status.append("AUTO")

                    found = True
                    break

                else:

                    print(
                        f"Outside Karnataka -> {row['police_station_name']}"
                    )

        except Exception:
            pass

    if not found:

        print(f"Manual Review -> {row['police_station_name']}")

        new_lat.append(row["latitude"])
        new_lon.append(row["longitude"])
        status.append("MANUAL")


df["latitude"] = new_lat
df["longitude"] = new_lon
df["geocode_status"] = status

df.to_csv(OUTPUT_FILE, index=False)

print("\nCompleted.")