#!/usr/bin/env python
"""
Populate database with sample data for testing and development.
"""
import os
import sys
import django
from datetime import datetime, timedelta
import random

# Add the Django app to the Python path
sys.path.insert(0, '/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vandine_monitor.settings')
django.setup()

from apps.network_monitor.models import Device, SystemMetric, Alert, NetworkScan
from django.utils import timezone
from django.conf import settings


def create_devices():
    """Create device entries from settings."""
    print("Creating devices...")
    
    devices_created = 0
    for device_config in settings.NETWORK_DEVICES:
        device, created = Device.objects.get_or_create(
            name=device_config['name'],
            defaults={
                'ip_address': device_config['host'],
                'device_type': device_config['device_type'],
                'username': device_config['username'],
                'password': device_config['password'],
                'is_active': True,
                'last_seen': timezone.now()
            }
        )
        if created:
            devices_created += 1
            print(f"  Created device: {device.name}")
        else:
            print(f"  Device already exists: {device.name}")
    
    return devices_created


def create_sample_metrics():
    """Create sample metrics for testing."""
    print("Creating sample metrics...")
    
    devices = Device.objects.all()
    metrics_created = 0
    
    # Create metrics for the last 24 hours
    now = timezone.now()
    for device in devices:
        for hours_ago in range(24, -1, -1):
            timestamp = now - timedelta(hours=hours_ago)
            
            # Create realistic looking metrics with some variation
            base_cpu = random.uniform(20, 40)
            base_memory = random.uniform(30, 50)
            base_disk = random.uniform(40, 60)
            
            metric = SystemMetric.objects.create(
                device=device,
                timestamp=timestamp,
                cpu_percent=round(base_cpu + random.uniform(-10, 10), 2),
                memory_percent=round(base_memory + random.uniform(-5, 5), 2),
                disk_percent=round(base_disk + random.uniform(-2, 2), 2),
                temperature=round(random.uniform(40, 55), 1) if 'pi' in device.name else None,
                uptime_seconds=86400 * random.randint(1, 30),
                load_average=[
                    round(random.uniform(0.5, 2.0), 2),
                    round(random.uniform(0.5, 1.5), 2),
                    round(random.uniform(0.5, 1.0), 2)
                ]
            )
            metrics_created += 1
    
    print(f"  Created {metrics_created} metrics")
    return metrics_created


def create_sample_alerts():
    """Create sample alerts for testing."""
    print("Creating sample alerts...")
    
    devices = Device.objects.all()
    alerts_created = 0
    
    alert_templates = [
        {
            'severity': 'warning',
            'title': 'High CPU Usage',
            'message': 'CPU usage exceeded 80% for more than 5 minutes'
        },
        {
            'severity': 'error',
            'title': 'Device Offline',
            'message': 'Device has not responded to health checks'
        },
        {
            'severity': 'info',
            'title': 'System Update Available',
            'message': 'New system updates are available for installation'
        },
        {
            'severity': 'critical',
            'title': 'Disk Space Critical',
            'message': 'Less than 10% disk space remaining'
        }
    ]
    
    # Create some alerts
    for device in devices:
        # Random chance of having alerts
        if random.random() > 0.5:
            alert_data = random.choice(alert_templates)
            alert = Alert.objects.create(
                device=device,
                severity=alert_data['severity'],
                title=alert_data['title'],
                message=f"{alert_data['message']} on {device.name}",
                is_resolved=random.random() > 0.7  # 70% chance of being unresolved
            )
            alerts_created += 1
    
    print(f"  Created {alerts_created} alerts")
    return alerts_created


def create_sample_network_scans():
    """Create sample network scan results."""
    print("Creating sample network scans...")
    
    scans_created = 0
    
    # Create scans for the last 7 days
    now = timezone.now()
    for days_ago in range(7, -1, -1):
        timestamp = now - timedelta(days=days_ago)
        
        # Morning scan
        scan = NetworkScan.objects.create(
            timestamp=timestamp.replace(hour=8, minute=0),
            scan_type='subnet_discovery',
            active_hosts=random.randint(5, 15),
            scan_duration=random.uniform(10, 30),
            results={
                'subnet': '192.168.1.0/24',
                'hosts_found': random.randint(5, 15),
                'scan_method': 'nmap -sn'
            }
        )
        scans_created += 1
        
        # Evening scan
        scan = NetworkScan.objects.create(
            timestamp=timestamp.replace(hour=20, minute=0),
            scan_type='subnet_discovery',
            active_hosts=random.randint(8, 20),
            scan_duration=random.uniform(10, 30),
            results={
                'subnet': '192.168.1.0/24',
                'hosts_found': random.randint(8, 20),
                'scan_method': 'nmap -sn'
            }
        )
        scans_created += 1
    
    print(f"  Created {scans_created} network scans")
    return scans_created


def main():
    """Main function to populate all data."""
    print("Starting data population...")
    print("-" * 50)
    
    # Create devices
    devices_created = create_devices()
    
    # Create sample data
    metrics_created = create_sample_metrics()
    alerts_created = create_sample_alerts()
    scans_created = create_sample_network_scans()
    
    print("-" * 50)
    print("Data population complete!")
    print(f"  Devices: {devices_created} created")
    print(f"  Metrics: {metrics_created} created")
    print(f"  Alerts: {alerts_created} created")
    print(f"  Network Scans: {scans_created} created")
    print("-" * 50)


if __name__ == '__main__':
    main()