import pandas as pd
from datetime import datetime

from backend.config.database import SessionLocal
from backend.models.occurrence_master import OccurrenceMaster


CSV_PATH = "datasets/masters/inv_occurrence_master.csv"


def import_occurrences():

    db = SessionLocal()

    try:

        df = pd.read_csv(CSV_PATH)

        db.query(OccurrenceMaster).delete()
        db.commit()

        for _, row in df.iterrows():

            occurrence = OccurrenceMaster(
                occurrence_id=row["occurrence_id"],
                case_id=row["case_id"],
                occurrence_datetime=datetime.fromisoformat(
                    str(row["occurrence_datetime"])
                ),
                time_slot=row["time_slot"],
                district=row["district"],
                taluk=row["taluk"],
                gram_panchayat=row["gram_panchayat"],
                village=row["village"],
                police_station=row["police_station"],
                crime_latitude=row["crime_latitude"],
                crime_longitude=row["crime_longitude"],
            )

            db.add(occurrence)

        db.commit()

        print(f"✅ Imported {len(df)} occurrence records.")

    finally:
        db.close()


if __name__ == "__main__":
    import_occurrences()