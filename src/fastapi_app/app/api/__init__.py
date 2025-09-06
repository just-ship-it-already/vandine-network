from fastapi import APIRouter
from .endpoints import devices, metrics, network, websocket

router = APIRouter()

router.include_router(devices.router, prefix="/devices", tags=["devices"])
router.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
router.include_router(network.router, prefix="/network", tags=["network"])
router.include_router(websocket.router, prefix="/ws", tags=["websocket"])