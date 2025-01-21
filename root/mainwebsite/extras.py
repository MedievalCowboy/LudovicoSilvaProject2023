import os
from datetime import datetime


def obtener_rol_mas_alto(user):
    # Jerarquía de roles asociando el nombre con un valor numérico (mas alto, mas rango)
    jerarquia_roles = [
        ('admin',99),
        ('ceo', 20),
        ('gerente', 2),
        ('empleado', 1)
    ]
    grupos_usuario = user.groups.values_list('name', flat=True)

    mapa_roles = dict(jerarquia_roles)

    max_valor = 0
    rol_mas_alto = None
    for grupo in grupos_usuario:
        if grupo in mapa_roles:
            valor_actual = mapa_roles[grupo]
            if valor_actual > max_valor:
                max_valor = valor_actual
                rol_mas_alto = grupo

    return rol_mas_alto


def generar_nombre_imagen(instance, filename, clase_modelo, campo_id, nombre_carpeta):

    ext = filename.split('.')[-1]
    if clase_modelo == 'usuario':
        new_filename = f"{clase_modelo}_{instance.user.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
    else:
        new_filename = f"{clase_modelo}_{getattr(instance, campo_id)}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
    return os.path.join('images',nombre_carpeta, new_filename)

