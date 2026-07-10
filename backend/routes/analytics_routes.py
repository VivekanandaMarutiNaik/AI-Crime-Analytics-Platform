from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.config.database import get_db
from backend.schemas.analytics_schema import AnalyticsInsightsResponse
from backend.services.analytics_service import get_ai_insights

router = APIRouter(
    prefix="/analytics",
    tags=["AI Analytics"]
)


@router.get(
    "/insights",
    response_model=AnalyticsInsightsResponse,
)
def analytics_insights(
    db: Session = Depends(get_db),
):
    return get_ai_insights(db)