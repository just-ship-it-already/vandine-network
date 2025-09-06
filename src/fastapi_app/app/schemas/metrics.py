from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime


class MetricBase(BaseModel):
    device_id: int
    metric_type: str
    value: float
    unit: str
    metadata: Optional[Dict[str, Any]] = {}


class MetricCreate(MetricBase):
    pass


class MetricResponse(MetricBase):
    id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True