from typing import Optional
from datetime import datetime
from .common import ORMBase


class ChargesheetResponse(ORMBase):
    chargesheet_id: str
    court_name: Optional[str]
    filing_date: Optional[datetime]
    chargesheet_status: Optional[str]