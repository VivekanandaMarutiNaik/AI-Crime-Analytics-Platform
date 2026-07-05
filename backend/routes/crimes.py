from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.config.database import SessionLocal
from backend.models.crime_case import CrimeCase

router = APIRouter()


# Database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/crimes")
def get_crimes(db: Session = Depends(get_db)):
    crimes = db.query(CrimeCase).limit(100).all()
    return crimes