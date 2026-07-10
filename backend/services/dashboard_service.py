from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.models.case_master import CaseMaster
from backend.models.investigation_master import InvestigationMaster
from backend.models.chargesheet_master import ChargesheetMaster
from backend.models.arrest_master import ArrestMaster
from backend.models.victim_master import VictimMaster
from backend.models.accused_master import AccusedMaster
from sqlalchemy import func, extract

def normalize_district(district: str | None):
    if not district:
        return None

    district = district.strip().lower()

    aliases = {
        "bangalore": "bengaluru",
        "bangalore city": "bengaluru",
        "bengaluru city": "bengaluru",

        "mysore": "mysuru",

        "bellary": "ballari",

        "gulbarga": "kalaburagi",

        "bijapur": "vijayapura",

        "hubli": "hubballi",

        "tumkur": "tumakuru",

        "shimoga": "shivamogga",

        "chikmagalur": "chikkamagaluru",

        "chikballapur": "chikkaballapura",
    }

    return aliases.get(district, district)

def apply_district_filter(query, district: str | None):
    district = normalize_district(district)

    if district:
        query = query.filter(
            CaseMaster.district.ilike(f"%{district}%")
        )

    return query

def get_dashboard_summary(
    db: Session,
    district: str | None = None,
):

    query = apply_district_filter(
        db.query(CaseMaster),
        district
    )

    total_cases = query.count()

    under_investigation_query = (
        db.query(InvestigationMaster)
        .join(
            CaseMaster,
            InvestigationMaster.case_id == CaseMaster.case_id
        )
    )

    under_investigation_query = apply_district_filter(
        under_investigation_query,
        district
    )

    under_investigation = (
        under_investigation_query
        .filter(
            InvestigationMaster.investigation_status == "Ongoing"
        )
        .count()
    )

    closed_cases_query = apply_district_filter(
        db.query(CaseMaster),
        district
    )

    closed_cases = (
        closed_cases_query
        .filter(CaseMaster.case_status == "Closed")
        .count()
    )

    chargesheets_filed = (
        db.query(func.count(ChargesheetMaster.case_id))
        .scalar()
    )

    arrests = (
        db.query(func.count(ArrestMaster.arrest_id))
        .scalar()
    )

    total_victims = (
        db.query(func.count(VictimMaster.victim_id))
        .scalar()
    )

    total_accused = (
        db.query(func.count(AccusedMaster.accused_person_id))
        .scalar()
    )

    return {
        "total_cases": total_cases,
        "under_investigation": under_investigation,
        "closed_cases": closed_cases,
        "chargesheets_filed": chargesheets_filed,
        "arrests": arrests,
        "total_victims": total_victims,
        "total_accused": total_accused,
    }

def get_crime_category_distribution(
    db: Session,
    district: str | None = None,
):

    query = apply_district_filter(
        db.query(
            CaseMaster.crime_category,
            func.count(CaseMaster.case_id).label("count"),
        ),
        district,
    )

    results = (
        query
        .group_by(CaseMaster.crime_category)
        .order_by(func.count(CaseMaster.case_id).desc())
        .all()
    )

    return {
        "data": [
            {
                "label": category,
                "count": count,
            }
            for category, count in results
        ]
    }

def get_crime_severity_distribution(db: Session):

    results = (
        db.query(
            CaseMaster.crime_severity,
            func.count(CaseMaster.case_id).label("count")
        )
        .group_by(CaseMaster.crime_severity)
        .order_by(func.count(CaseMaster.case_id).desc())
        .all()
    )

    return {
        "data": [
            {
                "label": severity,
                "count": count,
            }
            for severity, count in results
        ]
    }

def get_monthly_crime_trend(
    db: Session,
    district: str | None = None,
):

    query = apply_district_filter(
        db.query(
            extract("month", CaseMaster.crime_datetime).label("month"),
            func.count(CaseMaster.case_id).label("count"),
        ),
        district,
    )

    results = (
        query
        .group_by(extract("month", CaseMaster.crime_datetime))
        .order_by(extract("month", CaseMaster.crime_datetime))
        .all()
    )

    month_names = {
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Aug",
        9: "Sep",
        10: "Oct",
        11: "Nov",
        12: "Dec",
    }

    return {
        "data": [
            {
                "month": month_names[int(month)],
                "count": count,
            }
            for month, count in results
        ]
    }

def get_district_crime_distribution(db: Session):

    results = (
        db.query(
            CaseMaster.district,
            func.count(CaseMaster.case_id).label("count"),
        )
        .group_by(CaseMaster.district)
        .order_by(func.count(CaseMaster.case_id).desc())
        .all()
    )

    return {
        "data": [
            {
                "label": district,
                "count": count,
            }
            for district, count in results
        ]
    }

def get_case_status_distribution(
    db: Session,
    district: str | None = None,
):

    query = apply_district_filter(
        db.query(
            CaseMaster.case_status,
            func.count(CaseMaster.case_id).label("count"),
        ),
        district,
    )

    results = (
        query
        .group_by(CaseMaster.case_status)
        .order_by(func.count(CaseMaster.case_id).desc())
        .all()
    )

    return {
        "data": [
            {
                "label": status,
                "count": count,
            }
            for status, count in results
        ]
    }