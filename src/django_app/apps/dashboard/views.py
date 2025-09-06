from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.db import connection
import redis
from django.conf import settings


def index(request):
    """Main dashboard view."""
    context = {
        'title': 'Vandine Network Monitor',
        'devices': settings.NETWORK_DEVICES,
    }
    return render(request, 'dashboard/showcase_modern.html', context)


def health_check(request):
    """Health check endpoint for monitoring."""
    health_status = {
        'status': 'healthy',
        'database': 'unknown',
        'redis': 'unknown',
    }
    
    # Check database
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        health_status['database'] = 'healthy'
    except Exception as e:
        health_status['database'] = 'unhealthy'
        health_status['status'] = 'unhealthy'
        health_status['database_error'] = str(e)
    
    # Check Redis
    try:
        r = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
        )
        r.ping()
        health_status['redis'] = 'healthy'
    except Exception as e:
        health_status['redis'] = 'unhealthy'
        health_status['status'] = 'unhealthy'
        health_status['redis_error'] = str(e)
    
    return JsonResponse(health_status)