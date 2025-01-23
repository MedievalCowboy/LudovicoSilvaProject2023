# security/decorators.py
from django.shortcuts import redirect
from django.conf import settings
from .utils import obtener_rol_mas_alto
from .hierarchy import HIERARCHY

def role_required(*required_roles):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(f'{settings.LOGIN_URL}?next={request.path}')
            
            user_role = obtener_rol_mas_alto(request.user)
            
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
                
            if not required_roles:
                return redirect('error_500')

            try:
                required_values = [HIERARCHY[role] for role in required_roles]
                min_required = min(required_values)
                user_value = HIERARCHY.get(user_role, 0)
                
                if user_value >= min_required:
                    return view_func(request, *args, **kwargs)
                    
            except KeyError as e:
                print(f"Error de roles: {e}")
                return redirect('error_500')

            print(f"Acceso denegado: {request.user} - {request.path}")
            return redirect('error_500')

        return wrapper
    return decorator

def only_admin(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.is_staff:
                return view_func(request, *args, **kwargs)
            return redirect('ordenes')

        return wrapper_func