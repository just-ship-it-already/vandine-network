from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from ...core.database import get_db
from ...models import Device
from ...schemas.device import DeviceCreate, DeviceResponse, DeviceUpdate

router = APIRouter()


@router.get("/", response_model=List[DeviceResponse])
async def get_devices(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Get all devices."""
    result = await db.execute(
        select(Device).offset(skip).limit(limit)
    )
    devices = result.scalars().all()
    return devices


@router.get("/{device_id}", response_model=DeviceResponse)
async def get_device(
    device_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific device."""
    result = await db.execute(
        select(Device).where(Device.id == device_id)
    )
    device = result.scalar_one_or_none()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@router.post("/", response_model=DeviceResponse)
async def create_device(
    device: DeviceCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new device."""
    db_device = Device(**device.dict())
    db.add(db_device)
    await db.commit()
    await db.refresh(db_device)
    return db_device


@router.put("/{device_id}", response_model=DeviceResponse)
async def update_device(
    device_id: int,
    device_update: DeviceUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a device."""
    result = await db.execute(
        select(Device).where(Device.id == device_id)
    )
    device = result.scalar_one_or_none()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    for field, value in device_update.dict(exclude_unset=True).items():
        setattr(device, field, value)
    
    await db.commit()
    await db.refresh(device)
    return device


@router.delete("/{device_id}")
async def delete_device(
    device_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete a device."""
    result = await db.execute(
        select(Device).where(Device.id == device_id)
    )
    device = result.scalar_one_or_none()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    await db.delete(device)
    await db.commit()
    return {"message": "Device deleted successfully"}