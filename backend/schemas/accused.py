from typing import Optional
from .common import ORMBase


class AccusedResponse(ORMBase):
    accused_person_id: str
    accused_name: Optional[str]
    gender: Optional[str]
    age: Optional[int]
    occupation: Optional[str]
    is_arrested: Optional[bool]
    is_history_sheeter: Optional[bool]