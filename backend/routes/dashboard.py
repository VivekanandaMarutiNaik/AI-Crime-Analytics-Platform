from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional

from backend.config.database import get_db

from backend.schemas.dashboard import (
    DashboardSummary,
    CrimeCategoryResponse,
    CrimeSeverityResponse,
    MonthlyTrendResponse,
    DistrictCrimeResponse,
    CaseStatusResponse,
)

from backend.services.dashboard_service import (
    get_dashboard_summary,
    get_crime_category_distribution,
    get_crime_severity_distribution,
    get_monthly_crime_trend,
    get_district_crime_distribution,
    get_case_status_distribution,
)

router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"]
)


@router.get("/summary", response_model=DashboardSummary)
def dashboard_summary(
    district: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return get_dashboard_summary(db, district)

@router.get(
    "/crime-category",
    response_model=CrimeCategoryResponse,
)
def crime_category_distribution(
    district: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return get_crime_category_distribution(
        db,
        district,
    )

@router.get(
    "/crime-severity",
    response_model=CrimeSeverityResponse,
)
def crime_severity_distribution(
    district: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return get_crime_severity_distribution(
        db,
        district,
    )

@router.get(
    "/monthly-trend",
    response_model=MonthlyTrendResponse,
)
def monthly_crime_trend(
    district: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return get_monthly_crime_trend(
        db,
        district,
    )

@router.get(
    "/district-wise",
    response_model=DistrictCrimeResponse,
)
def district_wise_distribution(
    db: Session = Depends(get_db),
):
    return get_district_crime_distribution(db)

@router.get(
    "/case-status",
    response_model=CaseStatusResponse,
)
def case_status_distribution(
    district: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return get_case_status_distribution(
        db,
        district,
    )