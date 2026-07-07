from pathlib import Path

import pandas as pd
from fastapi import APIRouter

router = APIRouter(
    prefix="/api/cctv",
    tags=["CCTV"]
)

BASE_DIR = Path(__file__).resolve().parents[2]
DATASET_DIR = BASE_DIR / "datasets" / "processed"


@router.get("/existing")
def get_existing_cctv():
    df = pd.read_csv(DATASET_DIR / "cctv_master.csv")
    return df.to_dict(orient="records")


@router.get("/coverage")
def get_coverage():
    df = pd.read_csv(DATASET_DIR / "cctv_coverage_analysis.csv")
    return df.to_dict(orient="records")


@router.get("/recommendations")
def get_recommendations():
    df = pd.read_csv(DATASET_DIR / "cctv_installation_recommendations.csv")
    return df.to_dict(orient="records")