from pydantic import BaseModel


class HighestCrimeDistrict(BaseModel):
    district: str
    cases: int


class AnalyticsInsightsResponse(BaseModel):
    highest_crime_district: HighestCrimeDistrict
    arrest_rate: float
    chargesheet_rate: float
    fastest_growing_category: str
    cctv_coverage: float