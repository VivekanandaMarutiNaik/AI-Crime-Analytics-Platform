from typing import Optional
from datetime import datetime
from .common import ORMBase


class InvestigationResponse(ORMBase):
    investigation_id: str
    investigating_officer_id: Optional[str]
    investigation_start_date: Optional[datetime]
    investigation_end_date: Optional[datetime]
    investigation_status: Optional[str]