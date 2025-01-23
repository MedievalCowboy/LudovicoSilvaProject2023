from django import template

from mainwebsite.security.utils import obtener_rol_mas_alto
from mainwebsite.security.hierarchy import HIERARCHY, DISPLAY_NAMES

register = template.Library()

@register.filter(name='display_role')
def display_role(user):
    if not user.is_authenticated:
        return "Invitado"
    
    role = obtener_rol_mas_alto(user)
    
    # Manejar superusuarios
    if user.is_superuser and role != 'admin':
        return "Superusuario"
    
    return DISPLAY_NAMES.get(role, "Usuario Registrado")

@register.filter(name='has_higher_role')
def has_higher_role(user, target_role):
    # Verificar usuario autenticado
    if not user.is_authenticated:
        return False
    
    # Obtener y validar rol del usuario
    user_role = obtener_rol_mas_alto(user)
    if not user_role:
        return False
    
    # Normalizar nombres de roles
    target_role = target_role.strip().lower()
    
    # Comparar valores
    user_value = HIERARCHY.get(user_role, 0)
    target_value = HIERARCHY.get(target_role, 0)
    
    return user_value >= target_value

