import asyncio
from typing import Dict, List, Any
from netmiko import ConnectHandler
import psutil
from ..core.config import settings


class MetricsCollector:
    """Service for collecting system and network metrics."""
    
    def __init__(self):
        self.devices = [
            {
                'name': 'pi0',
                'host': settings.PI0_HOST,
                'username': settings.PI0_USERNAME,
                'password': settings.PI0_PASSWORD,
                'device_type': 'linux'
            },
            {
                'name': 'pi1',
                'host': settings.PI1_HOST,
                'username': settings.PI1_USERNAME,
                'password': settings.PI1_PASSWORD,
                'device_type': 'linux'
            }
        ]
    
    async def collect_all_metrics(self) -> Dict[str, Any]:
        """Collect metrics from all configured devices."""
        tasks = []
        for device in self.devices:
            task = asyncio.create_task(self.collect_device_metrics(device))
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        metrics = {}
        for device, result in zip(self.devices, results):
            if isinstance(result, Exception):
                metrics[device['name']] = {
                    'error': str(result),
                    'status': 'error'
                }
            else:
                metrics[device['name']] = result
        
        return metrics
    
    async def collect_device_metrics(self, device: Dict[str, str]) -> Dict[str, Any]:
        """Collect metrics from a single device via SSH."""
        try:
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            metrics = await loop.run_in_executor(
                None,
                self._collect_metrics_sync,
                device
            )
            return metrics
        except Exception as e:
            raise e
    
    def _collect_metrics_sync(self, device: Dict[str, str]) -> Dict[str, Any]:
        """Synchronous method to collect metrics via SSH."""
        try:
            # Connect to device
            connection = ConnectHandler(
                device_type=device['device_type'],
                host=device['host'],
                username=device['username'],
                password=device['password'],
                timeout=10
            )
            
            # Collect various metrics
            metrics = {
                'status': 'online',
                'host': device['host']
            }
            
            # CPU usage
            cpu_output = connection.send_command("top -bn1 | grep 'Cpu(s)'")
            if cpu_output:
                # Parse CPU usage
                parts = cpu_output.split()
                for i, part in enumerate(parts):
                    if 'id,' in part and i > 0:
                        idle = float(parts[i-1].replace('%', ''))
                        metrics['cpu_percent'] = round(100 - idle, 2)
                        break
            
            # Memory usage
            mem_output = connection.send_command("free -m | grep Mem")
            if mem_output:
                parts = mem_output.split()
                if len(parts) >= 3:
                    total = float(parts[1])
                    used = float(parts[2])
                    metrics['memory_percent'] = round((used / total) * 100, 2)
                    metrics['memory_mb'] = {'total': total, 'used': used}
            
            # Disk usage
            disk_output = connection.send_command("df -h / | tail -1")
            if disk_output:
                parts = disk_output.split()
                if len(parts) >= 5:
                    metrics['disk_percent'] = float(parts[4].replace('%', ''))
                    metrics['disk_gb'] = {
                        'total': parts[1],
                        'used': parts[2],
                        'available': parts[3]
                    }
            
            # Temperature (Raspberry Pi specific)
            temp_output = connection.send_command("vcgencmd measure_temp 2>/dev/null || echo 'temp=0'")
            if temp_output and 'temp=' in temp_output:
                temp = temp_output.split('=')[1].replace("'C", "")
                metrics['temperature_c'] = float(temp)
            
            # Uptime
            uptime_output = connection.send_command("uptime -s")
            if uptime_output:
                metrics['uptime'] = uptime_output.strip()
            
            connection.disconnect()
            return metrics
            
        except Exception as e:
            return {
                'status': 'offline',
                'error': str(e),
                'host': device['host']
            }
    
    async def collect_local_metrics(self) -> Dict[str, Any]:
        """Collect metrics from the local system."""
        return {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent,
            'network_io': psutil.net_io_counters()._asdict() if psutil.net_io_counters() else {}
        }