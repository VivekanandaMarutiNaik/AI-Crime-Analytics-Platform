from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.models.case_master import CaseMaster
from backend.models.occurrence_master import OccurrenceMaster


def get_all_crimes(
    db: Session,
    limit: int = 100,
    district: str | None = None,
):

    query = (
        db.query(
            CaseMaster,
            OccurrenceMaster,
        )
        .join(
            OccurrenceMaster,
            CaseMaster.case_id == OccurrenceMaster.case_id,
        )
    )

    if district:
        query = query.filter(
            CaseMaster.district.ilike(f"%{district}%")
        )

    results = (
        query
        .order_by(func.random())
        .limit(limit)
        .all()
    )
    return [
        {
            "case_id": case.case_id,
            "crime_datetime": case.crime_datetime,
            "crime_type": case.crime_type,
            "crime_category": case.crime_category,
            "crime_severity": case.crime_severity,
            "district": case.district,
            "taluk": case.taluk,
            "police_station": case.police_station,
            "case_status": case.case_status,

            "village": occurrence.village,
            "gram_panchayat": occurrence.gram_panchayat,

            "crime_latitude": occurrence.crime_latitude,
            "crime_longitude": occurrence.crime_longitude,
        }
        for case, occurrence in results
    ]


def get_districts(db: Session):

    districts = (
        db.query(CaseMaster.district)
        .distinct()
        .order_by(CaseMaster.district)
        .all()
    )

    return [d[0] for d in districts if d[0]]