from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from datetime import datetime, timedelta
from ...core.database import get_db
from ...models import NetworkMetric
from ...schemas.metrics import MetricCreate, MetricResponse

router = APIRouter()


@router.get("/", response_model=List[MetricResponse])
async def get_metrics(
    device_id: Optional[int] = Query(None),
    metric_type: Optional[str] = Query(None),
    hours: int = Query(24, description="Number of hours to look back"),
    db: AsyncSession = Depends(get_db)
):
    """Get network metrics with optional filtering."""
    query = select(NetworkMetric)
    
    # Filter by device
    if device_id:
        query = query.where(NetworkMetric.device_id == device_id)
    
    # Filter by metric type
    if metric_type:
        query = query.where(NetworkMetric.metric_type == metric_type)
    
    # Filter by time range
    time_threshold = datetime.utcnow() - timedelta(hours=hours)
    query = query.where(NetworkMetric.timestamp >= time_threshold)
    
    # Order by timestamp
    query = query.order_by(NetworkMetric.timestamp.desc()).limit(1000)
    
    result = await db.execute(query)
    metrics = result.scalars().all()
    return metrics


@router.post("/", response_model=MetricResponse)
async def create_metric(
    metric: MetricCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new metric entry."""
    db_metric = NetworkMetric(**metric.dict())
    db.add(db_metric)
    await db.commit()
    await db.refresh(db_metric)
    return db_metric


@router.get("/realtime/{device_id}")
async def get_realtime_metrics(
    device_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get the latest metrics for a device."""
    # Get the most recent metric for each type
    metric_types = ["bandwidth", "latency", "packet_loss"]
    latest_metrics = {}
    
    for metric_type in metric_types:
        result = await db.execute(
            select(NetworkMetric)
            .where(NetworkMetric.device_id == device_id)
            .where(NetworkMetric.metric_type == metric_type)
            .order_by(NetworkMetric.timestamp.desc())
            .limit(1)
        )
        metric = result.scalar_one_or_none()
        if metric:
            latest_metrics[metric_type] = {
                "value": metric.value,
                "unit": metric.unit,
                "timestamp": metric.timestamp
            }
    
    return latest_metrics