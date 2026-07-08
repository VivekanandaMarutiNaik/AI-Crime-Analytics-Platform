from pathlib import Path
from typing import Optional
import pandas as pd


DATASET_PATH = (
    Path(__file__).resolve().parents[2]
    / "datasets"
    / "processed"
    / "crime_hotspots.csv"
)

# Load once when the server starts
HOTSPOT_DF = pd.read_csv(DATASET_PATH)


def get_hotspots(district: Optional[str] = None):
    """
    Returns all hotspot locations.
    """

    hotspots = HOTSPOT_DF.copy()

    if district:
        hotspots = hotspots[
            hotspots["district"] == district
        ]

    records = hotspots.to_dict(orient="records")

    for row in records:
        for key, value in row.items():
            if pd.isna(value):
                row[key] = None

    return records

    for row in records:
        for key, value in row.items():
            if pd.isna(value):
                row[key] = None

    return records