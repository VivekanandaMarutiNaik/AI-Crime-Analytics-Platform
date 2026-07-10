from datetime import datetime

from .common import ORMBase


class CaseSummaryResponse(ORMBase):
    case_id: str

    crime_datetime: datetime

    district: str
    taluk: str
    police_station: str

    crime_category: str
    crime_type: str

    crime_severity: str

    case_status: str