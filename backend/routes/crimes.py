from fastapi import APIRouter, Query

from backend.services.crime_service import get_all_crimes

router = APIRouter(
    prefix="/crimes",
    tags=["Crimes"]
)


@router.get("")
def read_crimes(
    limit: int = Query(default=100, ge=1, le=1000),
    district: str | None = Query(default=None),
):
    """
    Returns crime records.
    """

    return get_all_crimes(
        limit=limit,
        district=district,
    )