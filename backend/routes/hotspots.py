from pathlib import Path

import pandas as pd
from fastapi import APIRouter

router = APIRouter(
    prefix="/api/hotspots",
    tags=["Hotspots"]
)

BASE_DIR = Path(__file__).resolve().parents[2]


@router.get("/")
def get_hotspots():
    df = pd.read_csv(
        BASE_DIR
        / "datasets"
        / "processed"
        / "crime_hotspots.csv"
    )

    return df.to_dict(orient="records")