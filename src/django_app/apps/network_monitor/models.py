from django.db import models


class Device(models.Model):
    """Network device model."""
    name = models.CharField(max_length=100, unique=True)
    ip_address = models.GenericIPAddressField()
    mac_address = models.CharField(max_length=17, blank=True, null=True)
    device_type = models.CharField(max_length=50, default='generic')
    is_active = models.BooleanField(default=True)
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.ip_address})"

    class Meta:
        ordering = ['name']


class SystemMetric(models.Model):
    """System metrics for a device."""
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='metrics')
    timestamp = models.DateTimeField(auto_now_add=True)
    cpu_percent = models.FloatField()
    memory_percent = models.FloatField()
    disk_percent = models.FloatField()
    temperature = models.FloatField(null=True, blank=True)
    
    class Meta:
        ordering = ['-timestamp']


class Alert(models.Model):
    """System alerts."""
    SEVERITY_CHOICES = [
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('critical', 'Critical'),
    ]
    
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='alerts')
    alert_type = models.CharField(max_length=50)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']