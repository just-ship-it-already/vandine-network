import asyncio
import subprocess
from typing import List, Dict
import ipaddress
import aiohttp


class NetworkScanner:
    """Service for network scanning operations."""
    
    async def scan_subnet(self, subnet: str) -> List[Dict[str, str]]:
        """Scan a subnet for active hosts using nmap."""
        try:
            # Run nmap scan asynchronously
            proc = await asyncio.create_subprocess_exec(
                'nmap', '-sn', subnet, '-oG', '-',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await proc.communicate()
            
            if proc.returncode != 0:
                print(f"Nmap error: {stderr.decode()}")
                return []
            
            # Parse nmap output
            active_hosts = []
            for line in stdout.decode().split('\n'):
                if 'Up' in line:
                    parts = line.split()
                    if len(parts) >= 2:
                        ip = parts[1]
                        active_hosts.append({
                            'ip': ip,
                            'status': 'up'
                        })
            
            return active_hosts
            
        except Exception as e:
            print(f"Network scan error: {e}")
            return []
    
    async def is_device_reachable(self, host: str, timeout: int = 3) -> bool:
        """Check if a device is reachable using ping."""
        try:
            proc = await asyncio.create_subprocess_exec(
                'ping', '-c', '1', '-W', str(timeout), host,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            await proc.communicate()
            return proc.returncode == 0
            
        except Exception:
            return False