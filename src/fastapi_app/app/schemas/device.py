from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DeviceBase(BaseModel):
    name: str
    ip_address: str
    device_type: str
    username: str
    password: str
    is_active: bool = True


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    ip_address: Optional[str] = None
    device_type: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None


class DeviceResponse(DeviceBase):
    id: int
    last_seen: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True