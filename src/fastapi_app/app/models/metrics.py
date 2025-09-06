from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base


class NetworkMetric(Base):
    __tablename__ = "network_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    metric_type = Column(String, nullable=False)  # bandwidth, latency, packet_loss
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=False)  # mbps, ms, percent
    metadata = Column(JSON, default={})
    
    # Relationships
    device = relationship("Device", backref="metrics")