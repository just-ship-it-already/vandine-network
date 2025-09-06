from django.db import models
from django.contrib.postgres.fields import ArrayField
import json


class Device(models.Model):
    """Network device model."""
    name = models.CharField(max_length=100, unique=True)
    ip_address = models.GenericIPAddressField()
    device_type = models.CharField(max_length=50)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)  # Should be encrypted in production
    is_active = models.BooleanField(default=True)
    last_seen = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.ip_address})"


class SystemMetric(models.Model):
    """System metrics for devices."""
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='metrics')
    timestamp = models.DateTimeField(auto_now_add=True)
    cpu_percent = models.FloatField()
    memory_percent = models.FloatField()
    disk_percent = models.FloatField()
    temperature = models.FloatField(null=True, blank=True)
    uptime_seconds = models.BigIntegerField()
    load_average = ArrayField(models.FloatField(), size=3, null=True, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['device', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.device.name} - {self.timestamp}"


class NetworkScan(models.Model):
    """Network scan results."""
    timestamp = models.DateTimeField(auto_now_add=True)
    scan_type = models.CharField(max_length=50)
    active_hosts = models.IntegerField(default=0)
    scan_duration = models.FloatField()  # seconds
    results = models.JSONField(default=dict)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"Scan at {self.timestamp}"


class Alert(models.Model):
    """System alerts."""
    SEVERITY_CHOICES = [
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('critical', 'Critical'),
    ]
    
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='alerts', null=True, blank=True)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.severity.upper()}: {self.title}"


class PerformanceTest(models.Model):
    """Network performance test results."""
    source_device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='perf_tests_source')
    target_device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='perf_tests_target')
    test_type = models.CharField(max_length=50)  # iperf3, ping, etc.
    timestamp = models.DateTimeField(auto_now_add=True)
    bandwidth_mbps = models.FloatField(null=True, blank=True)
    latency_ms = models.FloatField(null=True, blank=True)
    packet_loss_percent = models.FloatField(null=True, blank=True)
    jitter_ms = models.FloatField(null=True, blank=True)
    results = models.JSONField(default=dict)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.test_type}: {self.source_device} -> {self.target_device}"