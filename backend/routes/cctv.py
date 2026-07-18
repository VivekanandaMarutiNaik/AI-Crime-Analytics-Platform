from pathlib import Path

import pandas as pd
from fastapi import APIRouter
from typing import Optional

router = APIRouter(
    prefix="/api/cctv",
    tags=["CCTV"]
)

BASE_DIR = Path(__file__).resolve().parents[2]
DATASET_DIR = BASE_DIR / "datasets" / "processed"


import math

def dataframe_to_json(df):
    records = df.to_dict(orient="records")

    for row in records:
        for key, value in row.items():
            if pd.isna(value):
                row[key] = None

    return records


@router.get("/existing")
def get_existing_cctv(district: Optional[str] = None):
    df = pd.read_csv(DATASET_DIR / "cctv_master.csv")

    if district:
        df = df[df["district"] == district]

    return dataframe_to_json(df)


@router.get("/coverage")
def get_coverage(district: Optional[str] = None):
    df = pd.read_csv(DATASET_DIR / "cctv_coverage_analysis.csv")

    if district:
        df = df[df["district"] == district]

    return dataframe_to_json(df)

@router.get("/recommendations")
def get_recommendations(district: Optional[str] = None):
    df = pd.read_csv(DATASET_DIR / "cctv_installation_recommendations.csv")

    if district:
        df = df[df["district"] == district]

    return dataframe_to_json(df)