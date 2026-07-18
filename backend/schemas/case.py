from typing import List, Optional
from datetime import datetime

from .common import ORMBase
from .victim import VictimResponse
from .accused import AccusedResponse
from .investigation import InvestigationResponse
from .chargesheet import ChargesheetResponse


class CaseResponse(ORMBase):
    case_id: str

    crime_datetime: datetime

    district: str
    taluk: str
    police_station: str

    crime_category: str
    crime_type: str
    crime_severity: str

    case_status: str
    fir_registered: str

    victims: List[VictimResponse] = []

    accused: List[AccusedResponse] = []

    investigation: Optional[InvestigationResponse] = None

    chargesheet: Optional[ChargesheetResponse] = None