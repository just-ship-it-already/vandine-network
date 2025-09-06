from rest_framework import serializers
from apps.network_monitor.models import Device, SystemMetric, Alert, NetworkScan, PerformanceTest


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'name', 'ip_address', 'device_type', 'is_active', 'last_seen']
        read_only_fields = ['last_seen']


class SystemMetricSerializer(serializers.ModelSerializer):
    device_name = serializers.CharField(source='device.name', read_only=True)
    
    class Meta:
        model = SystemMetric
        fields = ['id', 'device', 'device_name', 'timestamp', 'cpu_percent', 
                  'memory_percent', 'disk_percent', 'temperature', 'uptime_seconds', 
                  'load_average']


class AlertSerializer(serializers.ModelSerializer):
    device_name = serializers.CharField(source='device.name', read_only=True, allow_null=True)
    
    class Meta:
        model = Alert
        fields = ['id', 'device', 'device_name', 'severity', 'title', 'message', 
                  'is_resolved', 'created_at', 'resolved_at']


class NetworkScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkScan
        fields = ['id', 'timestamp', 'scan_type', 'active_hosts', 'scan_duration', 'results']


class PerformanceTestSerializer(serializers.ModelSerializer):
    source_device_name = serializers.CharField(source='source_device.name', read_only=True)
    target_device_name = serializers.CharField(source='target_device.name', read_only=True)
    
    class Meta:
        model = PerformanceTest
        fields = ['id', 'source_device', 'source_device_name', 'target_device', 
                  'target_device_name', 'test_type', 'timestamp', 'bandwidth_mbps', 
                  'latency_ms', 'packet_loss_percent', 'jitter_ms', 'results']