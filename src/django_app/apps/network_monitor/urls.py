from django.urls import path
from . import views

app_name = 'network_monitor'

urlpatterns = [
    path('devices/', views.device_list, name='device_list'),
    path('metrics/', views.metrics_view, name='metrics'),
    path('alerts/', views.alerts_view, name='alerts'),
]