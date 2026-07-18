from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.config.database import get_db
from backend.services.crime_service import get_districts

router = APIRouter(
    tags=["Districts"],
)


@router.get("/districts")
def read_districts(
    db: Session = Depends(get_db),
):
    return get_districts(db)