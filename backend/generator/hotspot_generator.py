import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

crime = pd.read_csv(
    BASE_DIR / "datasets" / "raw" / "crime_cases.csv"
)

hotspots = (
    crime.groupby(
        [
            "district",
            "taluk",
            "police_station_name",
        ]
    )
    .agg(
        latitude=("crime_latitude", "mean"),
        longitude=("crime_longitude", "mean"),
        crime_count=("crime_id", "count"),
        avg_hotspot_score=("hotspot_score", "mean"),
    )
    .reset_index()
)

hotspots["recommended_cctv"] = (
    hotspots["crime_count"] / 8
).round().clip(lower=1).astype(int)

hotspots.rename(
    columns={
        "police_station_name": "police_station"
    },
    inplace=True,
)

# Keep only top hotspots in each district
hotspots = (
    hotspots.sort_values(
        "crime_count",
        ascending=False,
    )
    .groupby("district")
    .head(10)
)

hotspots["avg_hotspot_score"] = (
    hotspots["avg_hotspot_score"].round(1)
)

hotspots.to_csv(
    BASE_DIR
    / "datasets"
    / "processed"
    / "crime_hotspots.csv",
    index=False,
)

print(f"Generated {len(hotspots)} hotspots.")