from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'devices', views.DeviceViewSet)
router.register(r'metrics', views.SystemMetricViewSet)
router.register(r'alerts', views.AlertViewSet)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
]