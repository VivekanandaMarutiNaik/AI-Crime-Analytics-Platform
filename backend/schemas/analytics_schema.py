from pydantic import BaseModel
from typing import List


class HighestCrimeDistrict(BaseModel):
    district: str
    cases: int
class HighestCrimeCategory(BaseModel):
    category: str
    cases: int

class MostDangerousTaluk(BaseModel):
    taluk: str
    cases: int


class AnalyticsInsightsResponse(BaseModel):
    highest_crime_district: HighestCrimeDistrict
    highest_crime_category: HighestCrimeCategory
    arrest_rate: float
    chargesheet_rate: float
    fastest_growing_category: str
    cctv_coverage: float
    most_dangerous_taluk: MostDangerousTaluk
    peak_crime_time: str



class DistrictRiskScore(BaseModel):
    district: str
    risk_score: float
    risk_level: str


class RiskScoreResponse(BaseModel):
    data: List[DistrictRiskScore]

class OfficerWorkload(BaseModel):
    employee_id: str
    employee_name: str
    rank: str
    district: str
    assigned_cases: int
    ongoing_cases: int
    closed_cases: int
    workload_score: float
    workload_level: str
    recommendation: str


class OfficerWorkloadResponse(BaseModel):
    data: list[OfficerWorkload]

class InvestigationPerformance(BaseModel):
    district: str
    total_cases: int
    closed_cases: int
    ongoing_cases: int
    arrests: int
    chargesheets: int
    closure_rate: float
    arrest_rate: float
    chargesheet_rate: float
    performance_score: float
    grade: str


class InvestigationPerformanceResponse(BaseModel):
    data: list[InvestigationPerformance]

