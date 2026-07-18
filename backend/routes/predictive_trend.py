from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.config.database import get_db
from backend.services.predictive_trend_service import get_predictive_trend

router = APIRouter()


@router.get("/predictive-trend")
def predictive_trend(
    district: str | None = None,
    db: Session = Depends(get_db),
):
    return get_predictive_trend(db, district)