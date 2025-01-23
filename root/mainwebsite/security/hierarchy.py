HIERARCHY = {
    'admin': 100,
    'ceo': 80,
    'gerente': 50,
    'empleado': 10
}

# Diccionario de nombres amigables
DISPLAY_NAMES = {
    'admin': 'Administrador del Sistema',
    'ceo': 'Director General (CEO)',
    'gerente': 'Gerente Regional',
    'empleado': 'Empleado'
}

def get_role_value(role_name):
    return HIERARCHY.get(role_name, 0)

def get_allowed_roles(user_role):
    """Obtiene roles que puede asignar un usuario según su posición jerárquica"""
    user_value = get_role_value(user_role)
    return {role: value for role, value in HIERARCHY.items() if value <= user_value}

