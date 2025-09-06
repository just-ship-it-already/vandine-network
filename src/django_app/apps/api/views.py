from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.network_monitor.models import Device, SystemMetric, Alert
from .serializers import DeviceSerializer, SystemMetricSerializer, AlertSerializer


class DeviceViewSet(viewsets.ModelViewSet):
    """API endpoint for devices."""
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    @action(detail=True, methods=['get'])
    def metrics(self, request, pk=None):
        """Get metrics for a specific device."""
        device = self.get_object()
        metrics = device.metrics.all()[:100]  # Last 100 metrics
        serializer = SystemMetricSerializer(metrics, many=True)
        return Response(serializer.data)


class SystemMetricViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for system metrics."""
    queryset = SystemMetric.objects.all()
    serializer_class = SystemMetricSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        device_id = self.request.query_params.get('device')
        if device_id:
            queryset = queryset.filter(device_id=device_id)
        return queryset.order_by('-timestamp')[:1000]  # Limit to last 1000


class AlertViewSet(viewsets.ModelViewSet):
    """API endpoint for alerts."""
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        is_resolved = self.request.query_params.get('is_resolved')
        if is_resolved is not None:
            queryset = queryset.filter(is_resolved=is_resolved.lower() == 'true')
        return queryset
    
    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """Mark an alert as resolved."""
        alert = self.get_object()
        alert.is_resolved = True
        alert.save()
        serializer = self.get_serializer(alert)
        return Response(serializer.data)