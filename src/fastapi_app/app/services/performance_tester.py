import asyncio
import json
from typing import Dict, Any
import subprocess


class PerformanceTester:
    """Service for network performance testing."""
    
    async def run_iperf3_test(self, server_host: str, client_host: str, duration: int = 10) -> Dict[str, Any]:
        """Run iperf3 bandwidth test between two hosts."""
        try:
            # Run iperf3 test
            proc = await asyncio.create_subprocess_exec(
                'iperf3', '-c', server_host, '-t', str(duration), '-J',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await proc.communicate()
            
            if proc.returncode != 0:
                return {
                    'error': f"iperf3 failed: {stderr.decode()}",
                    'success': False
                }
            
            # Parse JSON output
            result = json.loads(stdout.decode())
            
            # Extract key metrics
            end_data = result.get('end', {})
            sum_sent = end_data.get('sum_sent', {})
            sum_received = end_data.get('sum_received', {})
            
            return {
                'success': True,
                'bandwidth_mbps': sum_sent.get('bits_per_second', 0) / 1_000_000,
                'bytes_transferred': sum_sent.get('bytes', 0),
                'duration': duration,
                'retransmits': sum_sent.get('retransmits', 0),
                'raw_data': result
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'success': False
            }
    
    async def run_ping_test(self, host: str, count: int = 10) -> Dict[str, Any]:
        """Run ping test to measure latency."""
        try:
            proc = await asyncio.create_subprocess_exec(
                'ping', '-c', str(count), host,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await proc.communicate()
            
            if proc.returncode != 0:
                return {
                    'error': f"Ping failed: {stderr.decode()}",
                    'success': False
                }
            
            # Parse ping output
            output = stdout.decode()
            lines = output.split('\n')
            
            # Extract statistics
            stats = {}
            for line in lines:
                if 'min/avg/max' in line:
                    # Parse RTT statistics
                    parts = line.split('=')[-1].strip().split('/')
                    if len(parts) >= 3:
                        stats['min_ms'] = float(parts[0])
                        stats['avg_ms'] = float(parts[1])
                        stats['max_ms'] = float(parts[2])
                elif '% packet loss' in line:
                    # Parse packet loss
                    loss = line.split('%')[0].split()[-1]
                    stats['packet_loss_percent'] = float(loss)
            
            return {
                'success': True,
                'host': host,
                'packets_sent': count,
                **stats
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'success': False
            }