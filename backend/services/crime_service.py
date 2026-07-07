from pathlib import Path

import pandas as pd


DATASET_PATH = (
    Path(__file__).resolve().parents[2]
    / "datasets"
    / "raw"
    / "crime_cases.csv"
)


def get_all_crimes(limit: int = 100):
    """
    Returns the first 'limit' crime records.
    """

    df = pd.read_csv(DATASET_PATH)

    return df.head(limit).to_dict(orient="records")