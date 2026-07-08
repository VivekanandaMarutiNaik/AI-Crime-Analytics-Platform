from fastapi import APIRouter
from typing import Optional

from backend.services.hotspot_service import get_hotspots

router = APIRouter(
    prefix="/hotspots",
    tags=["Hotspots"]
)


@router.get("")
def read_hotspots(district: Optional[str] = None):
    return get_hotspots(district)