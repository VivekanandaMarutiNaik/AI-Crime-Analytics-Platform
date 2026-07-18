from typing import Optional
from .common import ORMBase


class ArrestResponse(ORMBase):
    arrest_id: str
    arrest_date: Optional[str]
    arrest_status: Optional[str]