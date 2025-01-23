from .hierarchy import HIERARCHY

def obtener_rol_mas_alto(user):
    # Verificar usuario anónimo
    if user.is_anonymous:
        return None
    
    # Verificar superusuario
    if user.is_superuser:
        return 'admin'
    
    try:
        # Obtener grupos y validar existencia
        grupos = list(user.groups.values_list('name', flat=True))
        if not grupos:
            return None
            
        # Buscar máximo con manejo de errores
        return max(
            grupos,
            key=lambda x: HIERARCHY.get(x.lower().strip(), 0),
            default=None
        )
    except Exception as e:
        # Loggear error si es necesario
        return None

def puede_asignar_rol(assigner_role, target_role):
    return HIERARCHY.get(assigner_role, 0) >= HIERARCHY.get(target_role, 0)