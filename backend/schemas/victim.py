from typing import Optional
from .common import ORMBase


class VictimResponse(ORMBase):
    victim_id: str
    victim_name: str
    gender: Optional[str]
    age: Optional[int]
    occupation: Optional[str]