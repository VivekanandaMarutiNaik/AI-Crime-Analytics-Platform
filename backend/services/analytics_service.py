from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from pathlib import Path
import pandas as pd
from backend.models.case_master import CaseMaster
from backend.models.arrest_master import ArrestMaster
from backend.models.chargesheet_master import ChargesheetMaster
from datetime import timedelta
from backend.models.cctv_master import CCTVMaster
from backend.models.investigation_master import InvestigationMaster
from backend.models.employee_master import EmployeeMaster
from sqlalchemy import func, case

BASE_DIR = Path(__file__).resolve().parents[2]

CRIME_DATA = pd.read_csv(
    BASE_DIR / "datasets" / "raw" / "crime_cases.csv"
)

VIOLENT_CRIMES = {
    "Murder",
    "Attempt to Murder",
    "Rape",
    "Kidnapping",
    "Robbery",
    "Dacoity",
}

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

def get_highest_crime_category(db: Session):

    result = (
        db.query(
            CaseMaster.crime_category,
            func.count(CaseMaster.case_id).label("count")
        )
        .group_by(CaseMaster.crime_category)
        .order_by(func.count(CaseMaster.case_id).desc())
        .first()
    )

    if result is None:
        return {
            "category": "N/A",
            "cases": 0,
        }

    category, count = result

    return {
        "category": category,
        "cases": count,
    }

def get_most_dangerous_taluk(db: Session):

    result = (
        db.query(
            CaseMaster.taluk,
            func.count(CaseMaster.case_id).label("count"),
        )
        .filter(CaseMaster.taluk.isnot(None))
        .filter(CaseMaster.taluk != "")
        .group_by(CaseMaster.taluk)
        .order_by(func.count(CaseMaster.case_id).desc())
        .first()
    )

    if result is None:
        return {
            "taluk": "N/A",
            "cases": 0,
        }

    taluk, count = result

    return {
        "taluk": taluk,
        "cases": count,
    }
def get_peak_crime_time(db: Session):

    result = (
        db.query(
            extract("hour", CaseMaster.crime_datetime).label("hour"),
            func.count(CaseMaster.case_id).label("count"),
        )
        .group_by("hour")
        .order_by(func.count(CaseMaster.case_id).desc())
        .first()
    )

    if result is None:
        return "N/A"

    hour = int(result.hour)

    return f"{hour:02d}:00 - {(hour + 1) % 24:02d}:00"

    return {
        "taluk": taluk,
        "cases": count,
    }

    return {
        "category": category,
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
    print(CRIME_DATA.columns.tolist())

    return {
        "highest_crime_district": get_highest_crime_district(db),
        "highest_crime_category": get_highest_crime_category(db),
        "arrest_rate": get_arrest_rate(db),
        "chargesheet_rate": get_chargesheet_rate(db),
        "fastest_growing_category": get_fastest_growing_category(db),
        "cctv_coverage": get_cctv_coverage(db),
        "most_dangerous_taluk": get_most_dangerous_taluk(db),
        "peak_crime_time": get_peak_crime_time(db),
    }
def get_crime_risk_score(db: Session):

    districts = (
        db.query(CaseMaster.district)
        .distinct()
        .order_by(CaseMaster.district)
        .all()
    )

    results = []

    max_cases = (
        db.query(func.count(CaseMaster.case_id))
        .group_by(CaseMaster.district)
        .order_by(func.count(CaseMaster.case_id).desc())
        .first()[0]
    )

    for district in districts:

        district_name = district.district

        total_cases = (
            db.query(CaseMaster)
            .filter(
                CaseMaster.district == district_name
            )
            .count()
        )

        violent_cases = (
            db.query(CaseMaster)
            .filter(
                CaseMaster.district == district_name,
                CaseMaster.crime_category.in_(VIOLENT_CRIMES)
            )
            .count()
        )

        pending_investigations = (
            db.query(InvestigationMaster)
            .join(
                CaseMaster,
                InvestigationMaster.case_id == CaseMaster.case_id
            )
            .filter(
                CaseMaster.district == district_name,
                InvestigationMaster.investigation_status == "Ongoing"
            )
            .count()
        )

        arrests = (
            db.query(ArrestMaster)
            .join(
                CaseMaster,
                ArrestMaster.case_id == CaseMaster.case_id
            )
            .filter(
                CaseMaster.district == district_name
            )
            .count()
        )

        crime_volume = (
            (total_cases / max_cases) * 100
            if max_cases
            else 0
        )

        violent_ratio = (
            (violent_cases / total_cases) * 100
            if total_cases
            else 0
        )

        pending_ratio = (
            (pending_investigations / total_cases) * 100
            if total_cases
            else 0
        )

        arrest_gap = (
            (1 - (arrests / total_cases)) * 100
            if total_cases
            else 0
        )

        risk_score = round(
            (
                0.35 * crime_volume
                + 0.25 * violent_ratio
                + 0.20 * pending_ratio
                + 0.20 * arrest_gap
            ),
            2,
        )

        results.append(
            {
                "district": district_name,
                "risk_score": risk_score,
                "risk_level": get_risk_level(risk_score),
            }
        )
    
    scores = [r["risk_score"] for r in results]

    min_score = min(scores)
    max_score = max(scores)
    for r in results:

        if max_score == min_score:
            normalized = 50
        else:
            normalized = (
                (r["risk_score"] - min_score)
                / (max_score - min_score)
            ) * 100

        r["risk_score"] = round(normalized, 2)
        r["risk_level"] = get_risk_level(normalized)

    results.sort(
        key=lambda x: x["risk_score"],
        reverse=True,
    )

    return {
        "data": results
    }
    
def get_risk_level(score: float):

    if score >= 85:
        return "Critical"

    if score >= 70:
        return "High"

    if score >= 45:
        return "Medium"

    return "Low"

def get_workload_level(score: float):

    if score >= 80:
        return "High"

    if score >= 50:
        return "Medium"

    return "Low"




def get_officer_workload(db: Session):

    officers = db.query(EmployeeMaster).all()

    # Query 1: Assigned cases per officer
    assigned = dict(
        db.query(
            InvestigationMaster.investigating_officer_id,
            func.count(InvestigationMaster.investigation_id),
        )
        .group_by(InvestigationMaster.investigating_officer_id)
        .all()
    )

    # Query 2: Ongoing cases per officer
    ongoing = dict(
        db.query(
            InvestigationMaster.investigating_officer_id,
            func.count(InvestigationMaster.investigation_id),
        )
        .filter(
            InvestigationMaster.investigation_status == "Ongoing"
        )
        .group_by(InvestigationMaster.investigating_officer_id)
        .all()
    )

    results = []

    for officer in officers:

        assigned_cases = assigned.get(officer.employee_id, 0)
        ongoing_cases = ongoing.get(officer.employee_id, 0)

        if assigned_cases == 0:
            continue

        closed_cases = assigned_cases - ongoing_cases

        workload_score = min(
            round((assigned_cases / 25) * 100, 2),
            100,
        )

        level = get_workload_level(workload_score)

        if level == "High":
            recommendation = (
                "Reduce new case assignments and monitor workload closely."
            )
        elif level == "Medium":
            recommendation = (
                "Continue current workload with periodic monitoring."
            )
        else:
            recommendation = (
                "Officer has capacity to take additional investigations."
            )

        results.append(
            {
                "employee_id": officer.employee_id,
                "employee_name": officer.employee_name,
                "rank": officer.rank,
                "district": officer.district,
                "assigned_cases": assigned_cases,
                "ongoing_cases": ongoing_cases,
                "closed_cases": closed_cases,
                "workload_score": workload_score,
                "workload_level": level,
                "recommendation": recommendation,
            }
        )

    results.sort(
        key=lambda x: x["workload_score"],
        reverse=True,
    )

    return {
        "data": results
    }
def get_investigation_performance(db: Session):

    districts = (
        db.query(CaseMaster.district)
        .distinct()
        .order_by(CaseMaster.district)
        .all()
    )

    results = []

    for row in districts:

        district = row.district

        total_cases = (
            db.query(CaseMaster)
            .filter(CaseMaster.district == district)
            .count()
        )

        closed_cases = (
            db.query(CaseMaster)
            .filter(
                CaseMaster.district == district,
                CaseMaster.case_status == "Closed"
            )
            .count()
        )

        ongoing_cases = (
            db.query(InvestigationMaster)
            .join(
                CaseMaster,
                InvestigationMaster.case_id == CaseMaster.case_id
            )
            .filter(
                CaseMaster.district == district,
                InvestigationMaster.investigation_status == "Ongoing"
            )
            .count()
        )

        arrests = (
            db.query(ArrestMaster)
            .join(
                CaseMaster,
                ArrestMaster.case_id == CaseMaster.case_id
            )
            .filter(
                CaseMaster.district == district
            )
            .count()
        )

        chargesheets = (
            db.query(ChargesheetMaster)
            .join(
                CaseMaster,
                ChargesheetMaster.case_id == CaseMaster.case_id
            )
            .filter(
                CaseMaster.district == district
            )
            .count()
        )

        if total_cases == 0:
            continue

        closure_rate = round((closed_cases / total_cases) * 100, 2)
        arrest_rate = round((arrests / total_cases) * 100, 2)
        chargesheet_rate = round((chargesheets / total_cases) * 100, 2)

        raw_score = (
            closure_rate * 0.40
            + arrest_rate * 0.35
            + chargesheet_rate * 0.25
        )

        results.append(
            {
                "district": district,
                "total_cases": total_cases,
                "closed_cases": closed_cases,
                "ongoing_cases": ongoing_cases,
                "arrests": arrests,
                "chargesheets": chargesheets,
                "closure_rate": closure_rate,
                "arrest_rate": arrest_rate,
                "chargesheet_rate": chargesheet_rate,
                "performance_score": raw_score,
            }
        )

    # ----------------------------
    # Normalize AFTER all districts
    # ----------------------------

    scores = [r["performance_score"] for r in results]

    min_score = min(scores)
    max_score = max(scores)

    for r in results:

        if max_score == min_score:
            normalized = 50
        else:
            normalized = (
                (r["performance_score"] - min_score)
                / (max_score - min_score)
            ) * 100

        r["performance_score"] = round(normalized, 2)
        r["grade"] = get_performance_grade(normalized)

    results.sort(
        key=lambda x: x["performance_score"],
        reverse=True,
    )

    return {
        "data": results
    }
def get_performance_grade(score: float):

    if score >= 85:
        return "A"

    if score >= 70:
        return "B"

    if score >= 50:
        return "C"

    if score >= 30:
        return "D"

    return "E"
