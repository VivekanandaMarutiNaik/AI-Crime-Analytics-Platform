from fastapi import APIRouter
from backend.services.crime_service import get_districts

router = APIRouter(
    prefix="/districts",
    tags=["Districts"]
)


@router.get("")
def read_districts():
    return get_districts()