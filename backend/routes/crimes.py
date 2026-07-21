from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.config.database import get_db
from backend.services.crime_service import get_all_crimes

router = APIRouter(
    prefix="/crimes",
    tags=["Crimes"],
)


@router.get("")
def read_crimes(
    limit: int = Query(default=1000, ge=1, le=50000),
    district: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    print("District received:", district)
    return get_all_crimes(
        db=db,
        limit=limit,
        district=district,
    )