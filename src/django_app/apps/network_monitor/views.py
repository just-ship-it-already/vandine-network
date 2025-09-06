from django.shortcuts import render
from django.http import JsonResponse
from .models import Device, SystemMetric, Alert


def device_list(request):
    """List all network devices."""
    devices = Device.objects.filter(is_active=True)
    context = {
        'devices': devices,
    }
    return render(request, 'network_monitor/devices.html', context)


def metrics_view(request):
    """Display system metrics."""
    # Get latest metrics for each device
    devices = Device.objects.filter(is_active=True)
    metrics_data = []
    
    for device in devices:
        latest_metric = device.metrics.first()
        if latest_metric:
            metrics_data.append({
                'device': device,
                'metric': latest_metric,
            })
    
    context = {
        'metrics_data': metrics_data,
    }
    return render(request, 'network_monitor/metrics.html', context)


def alerts_view(request):
    """Display system alerts."""
    alerts = Alert.objects.filter(is_resolved=False)
    context = {
        'alerts': alerts,
    }
    return render(request, 'network_monitor/alerts.html', context)