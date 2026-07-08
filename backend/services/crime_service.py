from pathlib import Path

import pandas as pd

DATASET_PATH = (
    Path(__file__).resolve().parents[2]
    / "datasets"
    / "raw"
    / "crime_cases.csv"
)

# Load the dataset once when the server starts
CRIME_DF = pd.read_csv(DATASET_PATH)


def get_all_crimes(limit: int = 100, district: str | None = None):
    """
    Returns the first 'limit' crime records.
    """

    df = CRIME_DF.copy()

    if district:
        df = df[df["district"] == district]

    records = df.head(limit).to_dict(orient="records")

    for row in records:
        for key, value in row.items():
            if pd.isna(value):
                row[key] = None

    return records
def get_districts():
    """
    Returns all unique districts.
    """

    districts = (
        CRIME_DF["district"]
        .dropna()
        .sort_values()
        .unique()
        .tolist()
    )

    return districts