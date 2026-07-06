from pathlib import Path
import pandas as pd
from math import radians, sin, cos, sqrt, atan2

BASE_DIR = Path(__file__).resolve().parents[1]

CRIMES = pd.read_csv(
    BASE_DIR / "datasets" / "raw" / "crime_cases.csv"
)

CCTV = pd.read_csv(
    BASE_DIR / "datasets" / "processed" / "cctv_master.csv"
)


def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # Earth radius in meters

    lat1, lon1, lat2, lon2 = map(
        radians,
        [lat1, lon1, lat2, lon2]
    )

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        sin(dlat / 2) ** 2
        + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


# Select one crime
crime = CRIMES.iloc[0]

crime_lat = crime["crime_latitude"]
crime_lon = crime["crime_longitude"]

# Calculate distance to every CCTV
CCTV["distance_m"] = CCTV.apply(
    lambda row: haversine(
        crime_lat,
        crime_lon,
        row["latitude"],
        row["longitude"]
    ),
    axis=1
)

# Keep only CCTV cameras within 500 meters
nearby = CCTV[CCTV["distance_m"] <= 500]

nearest = nearby.sort_values("distance_m").head(5)

print("=" * 60)
print("CRIME ANALYSIS")
print("=" * 60)

print(f"Crime ID           : {crime['crime_id']}")
print(f"Crime Category     : {crime['crime_category']}")
print(f"Crime Type         : {crime['crime_type']}")
print(f"District           : {crime['district']}")
print(f"Police Station     : {crime['police_station_name']}")
print(
    f"Crime Coordinates  : "
    f"({crime_lat:.6f}, {crime_lon:.6f})"
)

print("\nNearest CCTV Cameras")
print("-" * 60)

if nearest.empty:
    print("\n⚠ No CCTV cameras found within 500 meters.")
    print("\nAI Recommendation:")
    print("- Install a CCTV at the nearest market.")
    print("- Install a CCTV at the nearest traffic junction.")
    print("- Install a CCTV near the bus stand.")
else:
    for i, (_, row) in enumerate(nearest.iterrows(), start=1):

        print(f"{i}. {row['cctv_name']}")
        print(f"   Distance : {row['distance_m']:.1f} meters")
        print(f"   Status   : {row['status']}")
        print(f"   Station  : {row['nearest_police_station']}")
        print()

active_count = (nearest["status"] == "Active").sum()

print("=" * 60)
print("AI COVERAGE ASSESSMENT")
print("=" * 60)

if nearest.empty:
    print("Coverage: POOR")
    print("Reason: No CCTV cameras within 500 meters.")
elif active_count >= 3:
    print("Coverage: GOOD")
    print(f"{active_count} active CCTV cameras are available nearby.")
elif active_count >= 1:
    print("Coverage: MODERATE")
    print(f"{active_count} active CCTV cameras are available nearby.")
else:
    print("Coverage: POOR")
    print("Nearby cameras exist but none are active.")