import json
import os
import time
import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page

# Simple rate limiter
last_test_time = {}

def get_system_info():
    try:
        # Get Raspberry Pi model
        with open('/proc/device-tree/model', 'r') as f:
            model = f.read().strip('\x00')
    except:
        model = 'Unknown'
    
    # Get CPU temp
    try:
        temp = subprocess.check_output(['vcgencmd', 'measure_temp']).decode()
        temp = temp.strip().split('=')[1].replace("'C", '°C')
    except:
        temp = 'N/A'
    
    # Get memory info
    try:
        with open('/proc/meminfo', 'r') as f:
            meminfo = f.read()
            total = int([line for line in meminfo.split('\n') if 'MemTotal' in line][0].split()[1]) // 1024
            free = int([line for line in meminfo.split('\n') if 'MemAvailable' in line][0].split()[1]) // 1024
    except:
        total, free = 0, 0
    
    # Get uptime
    try:
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.read().split()[0])
            days = int(uptime_seconds // 86400)
            hours = int((uptime_seconds % 86400) // 3600)
    except:
        days, hours = 0, 0
    
    return {
        'model': model,
        'temp': temp,
        'memory': {'total': total, 'free': free, 'used': total - free},
        'uptime': {'days': days, 'hours': hours}
    }

@cache_page(5)  # Cache for 5 seconds
def system_info(request):
    return JsonResponse(get_system_info())

@csrf_exempt
def performance_test(request):
    client_ip = request.META.get('REMOTE_ADDR', '')
    current_time = time.time()
    
    # Rate limit: 1 test per 30 seconds per IP
    if client_ip in last_test_time:
        if current_time - last_test_time[client_ip] < 30:
            return JsonResponse({'error': 'Rate limited. Try again in 30 seconds.'}, status=429)
    
    last_test_time[client_ip] = current_time
    
    # Simple performance test
    start = time.time()
    
    # Simulate some work
    data = []
    for i in range(1000):
        data.append(i ** 2)
    
    processing_time = (time.time() - start) * 1000  # ms
    
    return JsonResponse({
        'processing_time': round(processing_time, 2),
        'timestamp': int(current_time),
        'operations': 1000
    })

def index(request):
    from django.shortcuts import render
    return render(request, 'index.html')
