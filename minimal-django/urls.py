from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('api/system-info/', views.system_info),
    path('api/performance-test/', views.performance_test),
]
