from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.config.database import get_db
from backend.schemas.case import CaseResponse

from typing import Optional

from backend.schemas.pagination import PaginatedResponse
from backend.schemas.case_summary import CaseSummaryResponse
from backend.services.case_service import (
    get_case_details,
    get_cases,
)

router = APIRouter(
    prefix="/cases",
    tags=["Cases"]
)

@router.get(
    "",
    response_model=PaginatedResponse[CaseSummaryResponse],
)
def list_cases(
    page: int = 1,
    limit: int = 20,
    search: Optional[str] = None,
    district: Optional[str] = None,
    crime_category: Optional[str] = None,
    case_status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return get_cases(
        db=db,
        page=page,
        limit=limit,
        search=search,
        district=district,
        crime_category=crime_category,
        case_status=case_status,
    )


@router.get(
    "/{case_id}",
    response_model=CaseResponse,
)
def get_case(
    case_id: str,
    db: Session = Depends(get_db),
):
    return get_case_details(db, case_id)