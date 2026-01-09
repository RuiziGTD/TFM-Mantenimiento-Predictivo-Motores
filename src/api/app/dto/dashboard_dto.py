from pydantic import BaseModel
from typing import List

class UnitHealthDTO(BaseModel):
    unit_id: int
    rul: float
    status: str

class HealthOverviewDTO(BaseModel):
    total_units: int
    rul_min: float
    rul_mean: float
    rul_max: float
    critical_units: int
    warning_units: int
    ok_units: int

class HealthDashboardDTO(BaseModel):
    overview: HealthOverviewDTO
    units: List[UnitHealthDTO]
