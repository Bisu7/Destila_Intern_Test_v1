from pydantic import BaseModel
from datetime import date, datetime
from typing import List, Literal

class ExceptionResponse(BaseModel):
    id: int
    product_code: str
    date: date
    planned_units: float
    actual_units: int
    deficit_pct: float
    severity: str
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class ExceptionUpdate(BaseModel):
    status: Literal["acknowledged", "resolved"]

class TrendDay(BaseModel):
    date: date
    planned_units: float
    actual_units: int

class ExceptionDetailResponse(ExceptionResponse):
    last_7_days: List[TrendDay]
    