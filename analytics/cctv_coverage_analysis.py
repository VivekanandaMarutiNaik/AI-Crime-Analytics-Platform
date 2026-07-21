import pandas as pd
from math import radians, sin, cos, sqrt, atan2

# Load datasets
hotspots = pd.read_csv("datasets/processed/crime_hotspots.csv")
cctv = pd.read_csv("datasets/processed/cctv_master.csv")


def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # Earth radius in metres

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        sin(dlat / 2) ** 2
        + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c

results = []

for _, hotspot in hotspots.iterrows():

    nearest_distance = float("inf")

    for _, camera in cctv.iterrows():

        distance = haversine(
            hotspot["latitude"],
            hotspot["longitude"],
            camera["latitude"],
            camera["longitude"],
        )

        if distance < nearest_distance:
            nearest_distance = distance

    results.append({
        "police_station": hotspot["police_station"],
        "district": hotspot["district"],
        "taluk": hotspot["taluk"],
        "crime_count": hotspot["crime_count"],
        "latitude": hotspot["latitude"],
        "longitude": hotspot["longitude"],
        "nearest_cctv_distance_m": round(nearest_distance, 2),
        "covered": nearest_distance <= 150,
    })

coverage = pd.DataFrame(results)

recommendations = coverage[
    coverage["covered"] == False
].copy()

recommendations["priority"] = recommendations["crime_count"].apply(
    lambda x: (
        "Critical" if x >= 250 else
        "High" if x >= 150 else
        "Medium" if x >= 75 else
        "Low"
    )
)

recommendations["recommended_cameras"] = recommendations[
    "crime_count"
].apply(
    lambda x: max(1, round(x / 100))
)

print(coverage.head())

coverage.to_csv(
    "datasets/processed/cctv_coverage_analysis.csv",
    index=False,
)

print(
    "\nSaved coverage analysis to "
    "datasets/processed/cctv_coverage_analysis.csv"
)

print("\nCoverage Summary:")
print(coverage["covered"].value_counts())

recommendations.to_csv(
    "datasets/processed/cctv_installation_recommendations.csv",
    index=False,
)

print("\nTop CCTV Installation Recommendations:\n")

print(
    recommendations.sort_values(
        "crime_count",
        ascending=False
    ).head(20)
)

print("\nRecommendation Summary:")
print(recommendations["priority"].value_counts())