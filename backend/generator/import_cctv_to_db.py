import pandas as pd

from backend.config.database import SessionLocal
import backend.models

from backend.models.cctv_master import CCTVMaster

CSV_PATH = "datasets/processed/cctv_master.csv"

db = SessionLocal()

try:
    df = pd.read_csv(CSV_PATH)

    db.query(CCTVMaster).delete()
    db.commit()

    records = []

    for _, row in df.iterrows():

        records.append(
            CCTVMaster(
                cctv_id=row["cctv_id"],
                cctv_name=row["cctv_name"],
                district_id=row["district_id"],
                district=row["district"],
                taluk_id=row["taluk_id"],
                taluk=row["taluk"],
                gp_id=row["gp_id"],
                gram_panchayat=row["gram_panchayat"],
                village_id=row["village_id"],
                village=row["village"],
                latitude=row["latitude"],
                longitude=row["longitude"],
                location_type=row["location_type"],
                coverage_radius_meters=row["coverage_radius_meters"],
                status=row["status"],
                nearest_police_station=row["nearest_police_station"],
            )
        )

    db.bulk_save_objects(records)
    db.commit()

    print(f"Imported {len(records)} CCTV records successfully.")

finally:
    db.close()