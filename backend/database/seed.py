import random
from datetime import datetime, timedelta

from faker import Faker

from backend.config.database import SessionLocal
from backend.models.crime_case import CrimeCase
from backend.utils.master_data import (
    DISTRICTS,
    CRIME_TYPES,
    CASE_STATUS,
    OFFICER_NAMES,
)

print("Seed script started...")

fake = Faker("en_IN")
db = SessionLocal()

def random_date():
    start = datetime(2024, 1, 1)
    end = datetime(2026, 7, 1)
    diff = end - start
    return start + timedelta(days=random.randint(0, diff.days))

try:
    for i in range(1, 11):
        dt = random_date()

        crime = CrimeCase(
            case_id=f"CASE{i:05d}",
            fir_number=f"FIR2026{i:05d}",
            crime_type=random.choice(CRIME_TYPES),
            district=random.choice(DISTRICTS),
            police_station=fake.city() + " Police Station",
            incident_date=dt.date(),
            incident_time=dt.time(),
            latitude=round(random.uniform(11.5, 18.5), 6),
            longitude=round(random.uniform(74.0, 78.5), 6),
            status=random.choice(CASE_STATUS),
            officer_name=random.choice(OFFICER_NAMES),
            brief_facts=fake.sentence(),
        )

        db.add(crime)

    db.commit()
    print("✅ 10 crime records inserted successfully!")

except Exception as e:
    db.rollback()
    print("❌ Error:", e)

finally:
    db.close()