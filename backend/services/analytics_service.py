from sqlalchemy.orm import Session
from sqlalchemy import func, extract

from backend.models.case_master import CaseMaster
from backend.models.arrest_master import ArrestMaster
from backend.models.chargesheet_master import ChargesheetMaster
from datetime import timedelta
from backend.models.cctv_master import CCTVMaster

def get_highest_crime_district(db: Session):

    district, count = (
        db.query(
            CaseMaster.district,
            func.count(CaseMaster.case_id)
        )
        .group_by(CaseMaster.district)
        .order_by(func.count(CaseMaster.case_id).desc())
        .first()
    )

    return {
        "district": district,
        "cases": count,
    }

def get_arrest_rate(db: Session):

    total_cases = db.query(CaseMaster).count()

    total_arrests = db.query(ArrestMaster).count()

    if total_cases == 0:
        return 0

    return round((total_arrests / total_cases) * 100, 2)

def get_chargesheet_rate(db: Session):

    total_cases = db.query(CaseMaster).count()

    total_chargesheets = db.query(ChargesheetMaster).count()

    if total_cases == 0:
        return 0

    return round((total_chargesheets / total_cases) * 100, 2)

def get_fastest_growing_category(db: Session):

    latest_date = db.query(func.max(CaseMaster.crime_datetime)).scalar()

    if latest_date is None:
        return "N/A"

    six_months_ago = latest_date - timedelta(days=183)
    twelve_months_ago = latest_date - timedelta(days=366)

    recent = (
        db.query(
            CaseMaster.crime_category,
            func.count(CaseMaster.case_id)
        )
        .filter(CaseMaster.crime_datetime >= six_months_ago)
        .group_by(CaseMaster.crime_category)
        .all()
    )

    previous = (
        db.query(
            CaseMaster.crime_category,
            func.count(CaseMaster.case_id)
        )
        .filter(
            CaseMaster.crime_datetime >= twelve_months_ago,
            CaseMaster.crime_datetime < six_months_ago
        )
        .group_by(CaseMaster.crime_category)
        .all()
    )

    recent_dict = dict(recent)
    previous_dict = dict(previous)

    highest_growth = float("-inf")
    fastest_category = "N/A"

    for category, recent_count in recent_dict.items():

        previous_count = previous_dict.get(category, 0)

        if previous_count == 0:
            growth = recent_count
        else:
            growth = (
                (recent_count - previous_count)
                / previous_count
            ) * 100

        if growth > highest_growth:
            highest_growth = growth
            fastest_category = category

    return fastest_category

def get_cctv_coverage(db: Session):

    total_cctvs = db.query(CCTVMaster).count()

    if total_cctvs == 0:
        return 0.0

    operational = (
        db.query(CCTVMaster)
        .filter(CCTVMaster.status == "Active")
        .count()
    )

    return round(
        (operational / total_cctvs) * 100,
        2
    )

def get_ai_insights(db: Session):

    return {
        "highest_crime_district": get_highest_crime_district(db),
        "arrest_rate": get_arrest_rate(db),
        "chargesheet_rate": get_chargesheet_rate(db),
        "fastest_growing_category": get_fastest_growing_category(db),
        "cctv_coverage": get_cctv_coverage(db),
    }