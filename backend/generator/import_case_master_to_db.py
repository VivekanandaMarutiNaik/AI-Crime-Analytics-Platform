import pandas as pd
from datetime import datetime

from backend.config.database import SessionLocal
from backend.models.case_master import CaseMaster
from backend.models.occurrence_master import OccurrenceMaster

CSV_PATH = "datasets/masters/case_master.csv"


def import_cases():

    db = SessionLocal()

    try:

        df = pd.read_csv(CSV_PATH)

        print("Reading:", CSV_PATH)
        print(
            df.loc[
                df["case_id"] == "CR027949",
                ["case_id", "district", "taluk"]
            ].to_string(index=False)
        )
        for _, row in df.iterrows():

            case = db.get(CaseMaster, row["case_id"])

            if case is None:
                case = CaseMaster(case_id=row["case_id"])
                db.add(case)

            case.crime_datetime = datetime.fromisoformat(str(row["crime_datetime"]))
            case.district = row["district"]
            case.taluk = row["taluk"]
            case.police_station = row["police_station"]
            case.crime_category = row["crime_category"]
            case.crime_type = row["crime_type"]
            case.crime_severity = row["crime_severity"]
            case.case_status = row["case_status"]
            case.fir_registered = row["fir_registered"]
            case.act_id = row["act_id"]
            case.section_id = row["section_id"]
           

          

        db.commit()

        print(f"✅ Imported {len(df)} case records.")

    finally:
        db.close()


if __name__ == "__main__":
    import_cases()