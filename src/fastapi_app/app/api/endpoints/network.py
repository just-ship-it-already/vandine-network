from fastapi import APIRouter, Depends, BackgroundTasks
from typing import Dict, List
import asyncio
from ...services.network_scanner import NetworkScanner
from ...services.performance_tester import PerformanceTester
from ...core.config import settings

router = APIRouter()

# Initialize services
network_scanner = NetworkScanner()
perf_tester = PerformanceTester()


@router.get("/scan")
async def scan_network():
    """Perform a network scan to discover active devices."""
    results = await network_scanner.scan_subnet("192.168.1.0/24")
    return {
        "active_hosts": len(results),
        "devices": results
    }


@router.post("/test/bandwidth")
async def test_bandwidth(
    source: str,
    target: str,
    duration: int = 10
):
    """Run bandwidth test between two devices."""
    result = await perf_tester.run_iperf3_test(source, target, duration)
    return result


@router.post("/test/latency")
async def test_latency(
    target: str,
    count: int = 10
):
    """Test network latency to a target."""
    result = await perf_tester.run_ping_test(target, count)
    return result


@router.get("/devices/status")
async def get_device_status():
    """Get current status of all configured devices."""
    devices = [
        {"name": "pi0", "host": settings.PI0_HOST},
        {"name": "pi1", "host": settings.PI1_HOST},
        {"name": "router", "host": settings.ROUTER_HOST},
    ]
    
    status_results = []
    for device in devices:
        is_reachable = await network_scanner.is_device_reachable(device["host"])
        status_results.append({
            "name": device["name"],
            "host": device["host"],
            "status": "online" if is_reachable else "offline"
        })
    
    return status_results