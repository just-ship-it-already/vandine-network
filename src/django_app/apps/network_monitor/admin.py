from django.contrib import admin
from .models import Device, SystemMetric, Alert

admin.site.register(Device)
admin.site.register(SystemMetric)
admin.site.register(Alert)
