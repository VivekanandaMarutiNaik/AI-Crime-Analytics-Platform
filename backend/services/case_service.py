from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from backend.models.case_master import CaseMaster
from backend.models.accused_master import AccusedMaster
from sqlalchemy import or_

def get_case_details(db: Session, case_id: str):
    case = (
        db.query(CaseMaster)
        .options(
            joinedload(CaseMaster.victims),
            joinedload(CaseMaster.accused).joinedload(AccusedMaster.arrest),
            joinedload(CaseMaster.investigation),
            joinedload(CaseMaster.chargesheet),
        )
        .filter(CaseMaster.case_id == case_id)
        .first()
    )

    if case is None:
        raise HTTPException(
            status_code=404,
            detail="Case not found"
        )

    return case

def get_cases(
    db: Session,
    page: int = 1,
    limit: int = 20,
    search: str | None = None,
    district: str | None = None,
    crime_category: str | None = None,
    case_status: str | None = None,
):
    query = db.query(CaseMaster)

    if search:
        query = query.filter(
            or_(
                CaseMaster.case_id.ilike(f"%{search}%"),
                CaseMaster.crime_type.ilike(f"%{search}%"),
                CaseMaster.crime_category.ilike(f"%{search}%"),
                CaseMaster.police_station.ilike(f"%{search}%"),
                CaseMaster.district.ilike(f"%{search}%"),
                CaseMaster.taluk.ilike(f"%{search}%"),
                CaseMaster.case_status.ilike(f"%{search}%"),
            )
        )

    if district:
        query = query.filter(
            CaseMaster.district.ilike(f"%{district}%")
        )

    if crime_category:
        query = query.filter(
            CaseMaster.crime_category.ilike(f"%{crime_category}%")
        )

    if case_status:
        query = query.filter(
            CaseMaster.case_status.ilike(f"%{case_status}%")
        )

    total = query.count()

    cases = (
        query.order_by(CaseMaster.crime_datetime.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "data": cases,
    }