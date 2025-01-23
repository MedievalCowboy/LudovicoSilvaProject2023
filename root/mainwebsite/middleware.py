from django.utils import timezone
from .models import UserSession
import threading
class UpdateLastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if request.user.is_authenticated:
            # Actualizar marca de tiempo de última actividad
            UserSession.objects.filter(
                user=request.user,
                session_key=request.session.session_key
            ).update(last_activity=timezone.now())
        
        return response
    



_local = threading.local()

class AuditMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _local.request = request
        response = self.get_response(request)
        del _local.request
        return response

def get_current_request():
    return getattr(_local, 'request', None)