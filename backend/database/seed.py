import pandas as pd

from backend.config.database import SessionLocal
from backend.models.case_master import CaseMaster
from backend.models.victim_master import VictimMaster
from backend.models.accused_master import AccusedMaster
from backend.models.investigation_master import InvestigationMaster
from backend.models.arrest_master import ArrestMaster
from backend.models.chargesheet_master import ChargesheetMaster
from backend.models.employee_master import EmployeeMaster


db = SessionLocal()


def load_csv(model, csv_path, date_columns=None):
    print(f"\nLoading {csv_path}...")

    df = pd.read_csv(csv_path)

    if date_columns:
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce")
                df[col] = df[col].astype(object)
                df[col] = df[col].where(df[col].notna(), None)

    records = df.to_dict(orient="records")

    objects = [model(**record) for record in records]

    db.bulk_save_objects(objects)
    db.commit()

    print(f"✅ Imported {len(objects)} records")


def main():
    try:

        load_csv(
            EmployeeMaster,
            "datasets/masters/employee_master.csv",
            ["date_of_birth", "appointment_date"],
        )

        load_csv(
            CaseMaster,
            "datasets/masters/case_master.csv",
            ["crime_datetime"],
        )

        load_csv(
            VictimMaster,
            "datasets/masters/victim_master.csv",
        )

        load_csv(
            AccusedMaster,
            "datasets/masters/accused_master.csv",
        )

        load_csv(
            InvestigationMaster,
            "datasets/masters/investigation_master.csv",
            [
                "investigation_start_date",
                "investigation_end_date",
            ],
        )

        load_csv(
            ArrestMaster,
            "datasets/masters/arrest_master.csv",
            [
                "arrest_date",
            ],
        )

        load_csv(
            ChargesheetMaster,
            "datasets/masters/chargesheet_master.csv",
            [
                "filing_date",
            ],
        )

        print("\n🎉 Database seeding completed successfully!")

    except Exception as e:
        db.rollback()
        print(e)

    finally:
        db.close()


if __name__ == "__main__":
    main()