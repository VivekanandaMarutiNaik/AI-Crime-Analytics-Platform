from pydantic import BaseModel


class DashboardSummary(BaseModel):
    total_cases: int
    under_investigation: int
    closed_cases: int
    chargesheets_filed: int
    arrests: int
    total_victims: int
    total_accused: int

class ChartItem(BaseModel):
    label: str
    count: int


class CrimeCategoryResponse(BaseModel):
    data: list[ChartItem]

class CrimeSeverityResponse(BaseModel):
    data: list[ChartItem]

class MonthlyTrendItem(BaseModel):
    month: str
    count: int


class MonthlyTrendResponse(BaseModel):
    data: list[MonthlyTrendItem]

class DistrictCrimeResponse(BaseModel):
    data: list[ChartItem]

class CaseStatusResponse(BaseModel):
    data: list[ChartItem]