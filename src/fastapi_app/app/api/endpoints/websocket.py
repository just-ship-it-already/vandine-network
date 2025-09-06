from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
import asyncio
import json
from ...services.metrics_collector import MetricsCollector

router = APIRouter()

# Store active connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
    
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()
metrics_collector = MetricsCollector()


@router.websocket("/metrics")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time metrics streaming."""
    await manager.connect(websocket)
    try:
        # Start sending metrics
        while True:
            # Collect metrics from all devices
            metrics = await metrics_collector.collect_all_metrics()
            
            # Send metrics to client
            await websocket.send_json({
                "type": "metrics_update",
                "data": metrics
            })
            
            # Wait before next update
            await asyncio.sleep(5)  # Update every 5 seconds
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        manager.disconnect(websocket)
        print(f"WebSocket error: {e}")