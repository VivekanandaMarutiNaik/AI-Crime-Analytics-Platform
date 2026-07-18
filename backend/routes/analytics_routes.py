from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.config.database import get_db
from backend.schemas.analytics_schema import (
    AnalyticsInsightsResponse,
    RiskScoreResponse,
    OfficerWorkloadResponse,
    InvestigationPerformanceResponse,
)

from backend.services.analytics_service import (
    get_ai_insights,
    get_crime_risk_score,
    get_officer_workload,
    get_investigation_performance,
)

from backend.routes.predictive_trend import router as predictive_router
router = APIRouter(
    prefix="/analytics",
    tags=["AI Analytics"]
)


@router.get(
    "/ai-insights",
    response_model=AnalyticsInsightsResponse,
)
def analytics_insights(
    db: Session = Depends(get_db),
):
    return get_ai_insights(db)

@router.get(
    "/risk-score",
    response_model=RiskScoreResponse,
)
def crime_risk_score(
    db: Session = Depends(get_db),
):
    return get_crime_risk_score(db)

@router.get(
    "/officer-workload",
    response_model=OfficerWorkloadResponse,
)
def officer_workload(
    db: Session = Depends(get_db),
):
    return get_officer_workload(db)

@router.get(
    "/investigation-performance",
    response_model=InvestigationPerformanceResponse,
)
def investigation_performance(
    db: Session = Depends(get_db),
):
    return get_investigation_performance(db)

router.include_router(
    predictive_router,
    tags=["AI Analytics"]
)