print("Running NEW seed.py")
import pandas as pd

from backend.config.database import SessionLocal
from backend.models.crime_case import CrimeCase

# Load CSV
df = pd.read_csv("datasets/raw/crime_cases.csv")

db = SessionLocal()

try:
    for _, row in df.iterrows():
        print(CrimeCase.__table__.columns.keys())
        crime = CrimeCase(
            crime_id=row["crime_id"],
            crime_datetime=row["crime_datetime"],
            time_slot=row["time_slot"],
            district=row["district"],
            taluk=row["taluk"],
            village=row["village"],
            gram_panchayat=row["gram_panchayat"],

            police_station_name=row["police_station_name"],
            police_station_latitude=(
                0.0 if pd.isna(row["police_station_latitude"])
                else float(row["police_station_latitude"])
            ),

            police_station_longitude=(
                0.0 if pd.isna(row["police_station_longitude"])
                else float(row["police_station_longitude"])
            ),

            crime_category=row["crime_category"],
            crime_type=row["crime_type"],
            crime_severity=row["crime_severity"],

            hotspot_score=int(row["hotspot_score"]),

            victim_age=int(row["victim_age"]),
            victim_gender=row["victim_gender"],

            accused_id=row["accused_id"],
            accused_age=int(row["accused_age"]),
            accused_gender=row["accused_gender"],

            fir_registered=row["fir_registered"],
            case_status=row["case_status"],

            cctv_available=row["cctv_available"],

            response_time_minutes=int(row["response_time_minutes"])
        )

        db.add(crime)

    db.commit()
    print("✅ Successfully imported crime dataset!")

except Exception as e:
    db.rollback()
    print("❌ Error:", e)

finally:
    db.close()