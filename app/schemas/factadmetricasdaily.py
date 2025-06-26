from pydantic import BaseModel, Field, model_validator
from typing import Optional
from datetime import date
from fastapi import HTTPException

class FactAdMetricsCreate(BaseModel):
    date_id: int
    region_id: int
    age_id: int
    gender_id: int
    platform_id: int
    placement_id: int
    device_type_id: int
    impressions: int
    clicks: int
    cost: float
    conversions: int
    likes: int

class AdMetricFilter(BaseModel):
    start_date: date = Field(..., description="Format: YYYY-MM-DD")
    end_date: date = Field(..., description="Format: YYYY-MM-DD")
    
    region: Optional[str] = None
    age_group: Optional[str] = None
    gender: Optional[str] = None
    platform: Optional[str] = None
    placement: Optional[str] = None
    device_type: Optional[str] = None

    impressions: Optional[int] = None
    clicks: Optional[int] = None
    cost: Optional[float] = None
    conversions: Optional[int] = None
    likes: Optional[int] = None

    @model_validator(mode='after')
    def validate_dates(self) -> 'AdMetricFilter':
        if self.start_date > self.end_date:
            raise HTTPException(status_code=400, detail="start_date cannot be greater than end_date")
        return self
