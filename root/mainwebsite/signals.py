from django.db import transaction
from django.db.models.signals import post_save, post_delete, pre_save

from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields.files import FieldFile

from .models import Profile, LoginHistory, UserSession, AuditLog, ProductoDestino, Orden_Producto
from .extras import get_client_ip, parse_user_agent
from .middleware import get_current_request

import datetime
from decimal import Decimal




def track_model(sender, **kwargs):
    """Registra señales para cualquier modelo a auditar"""
    
    # Capturar el estado ANTES de guardar (pre_save)
    @receiver(pre_save, sender=sender, weak=False)
    def pre_save_handler(sender, instance, **kwargs):
        if instance.pk:  # Solo para actualizaciones(updates)
            try:
                instance._old_state = sender.objects.get(pk=instance.pk)
            except sender.DoesNotExist:
                instance._old_state = None
        else:  # Creación si no hay estado anterior
            instance._old_state = None
    
    # Procesar después de guardar (post_save)
    @receiver(post_save, sender=sender, weak=False)
    def post_save_handler(sender, instance, created, **kwargs):
        request = get_current_request()
        
        ip = get_client_ip(request) if request else None
        ua_data = parse_user_agent(request) if request else {}
        
        # Obtener el estado anterior desde el atributo temporal
        old_instance = getattr(instance, '_old_state', None)
        
        AuditLog.objects.create(
            user=request.user if request and request.user.is_authenticated else None,
            content_type=ContentType.objects.get_for_model(sender),
            object_id=instance.pk,
            action='C' if created else 'U',
            changes=_get_changes(instance, old_instance) if not created else {},
            ip_address=ip,
            user_agent=ua_data
        )
        
        # Limpiar el atributo temporal
        if hasattr(instance, '_old_state'):
            del instance._old_state

    # Manejar eliminaciones (post_delete)
    @receiver(post_delete, sender=sender, weak=False)
    def post_delete_handler(sender, instance, **kwargs):
        request = get_current_request()
        ip = get_client_ip(request) if request else None
        
        AuditLog.objects.create(
            user=request.user if request and request.user.is_authenticated else None,
            content_type=ContentType.objects.get_for_model(sender),
            object_id=instance.pk,
            action='D',
            ip_address=ip,
            user_agent=parse_user_agent(request) if request else {}
        )

def _get_changes(instance, old_instance):
    """Compara el estado actual con el anterior, manejando tipos de datos."""
    if hasattr(instance, 'get_changes'):
        return instance.get_changes()
    
    if not old_instance:  # No hay estado anterior (creación)
        return {}
    
    changes = {}
    default_exclusions = {'id', 'creado_en', 'ultima_modificacion'}
    model_exclusions = set()
    
    if hasattr(instance, 'Audit') and hasattr(instance.Audit, 'excluded_fields'):
        model_exclusions = set(instance.Audit.excluded_fields)
    
    excluded_fields = default_exclusions.union(model_exclusions)
    
    for field in instance._meta.get_fields():
        if field.many_to_many or field.one_to_many:
            continue
            
        field_name = field.name
        if field_name in excluded_fields:
            continue
        
        try:
            old_val = getattr(old_instance, field_name, None)
            new_val = getattr(instance, field_name, None)
            
            # Manejar campos de archivo antes de la serialización
            if isinstance(old_val, FieldFile):
                old_val = old_val.name if old_val else None
            if isinstance(new_val, FieldFile):
                new_val = new_val.name if new_val else None
            
            if field.is_relation:
                old_val = old_val.pk if old_val else None
                new_val = new_val.pk if new_val else None
            else:
                # Aplicar serialización
                old_val = _serialize_value(old_val)
                new_val = _serialize_value(new_val)
            
            if old_val != new_val:
                changes[field_name] = {
                    'old': old_val,
                    'new': new_val
                }
        except Exception as e:
            continue  # Ignorar errores en campos problemáticos
    
    return changes

def _serialize_value(value):
    """Convierte valores complejos a tipos serializables para JSON."""
    if isinstance(value, (datetime.date, datetime.datetime)):
        return value.isoformat()
    elif hasattr(value, 'pk'):  # Para ForeignKey, etc.
        return value.pk
    elif isinstance(value, Decimal):
        return str(value)
    elif isinstance(value, float):
        return float(value)
    elif isinstance(value, FieldFile):  # Manejo de campos File/Image <- para imaggenes
        return value.name if value else None  # Devuelve el path relativo
    return value


@receiver([post_save, post_delete], sender=Orden_Producto)
def actualizar_reposiciones(sender, instance, **kwargs):
    """
    Actualiza la última reposición cuando se modifica una relación Orden-Producto
    """
    orden = instance.id_orden
    producto = instance.producto
    
    # Verificar si la orden tiene los datos necesarios
    if orden.fecha_entrega and orden.id_destino and producto:
        # Obtener la última fecha de entrega para este producto-destino
        ultima_entrega = Orden_Producto.objects.filter(
            producto=producto,
            id_orden__id_destino=orden.id_destino,
            id_orden__fecha_entrega__isnull=False
        ).order_by('-id_orden__fecha_entrega').first()

        if ultima_entrega:
            # Actualizar o crear el registro de reposición
            ProductoDestino.objects.update_or_create(
                producto=producto,
                destino=orden.id_destino,
                defaults={
                    'ultima_reposicion': ultima_entrega.id_orden.fecha_entrega,
                    'frecuencia_reposicion': 30  # Valor por defecto o cálculo personalizado
                }
            )
        else:
            # Eliminar el registro si ya no hay órdenes relacionadas
            ProductoDestino.objects.filter(
                producto=producto,
                destino=orden.id_destino
            ).delete()

@receiver(post_save,sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        print("Profile created.")


@receiver(post_save, sender=User)
def update_profile(sender, instance, created, **kwargs):
    if not created:
        instance.profile.save()
        print('Profile updated.')


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    with transaction.atomic():
        ip = get_client_ip(request)
        agent_info = parse_user_agent(request)
        
        LoginHistory.objects.create(
            user=user,
            event_type='login',
            ip_address=ip,
            user_agent=agent_info['user_agent'],
            device_type=agent_info['device_type'],
            browser=agent_info['browser'],
            operating_system=agent_info['os']
        )

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    with transaction.atomic():
        # Solo registrar logout si el usuario estaba autenticado
        if user.is_authenticated:
            ip = get_client_ip(request)
            agent_info = parse_user_agent(request)
            
            LoginHistory.objects.create(
                user=user,
                event_type='logout',
                ip_address=ip,
                user_agent=agent_info['user_agent'],
                device_type=agent_info['device_type'],
                browser=agent_info['browser'],
                operating_system=agent_info['os']
            )
            
            

@receiver(user_logged_in)
def create_user_session(sender, request, user, **kwargs):
    # Eliminar sesiones previas del usuario
    UserSession.objects.filter(user=user).delete()
    
    # Obtener información del dispositivo
    user_agent = parse_user_agent(request)
    device_info = f"{user_agent['device_type']}-{user_agent['os']}"
    
    # Crear nueva sesión
    UserSession.objects.create(
        user=user,
        session_key=request.session.session_key,
        ip_address=get_client_ip(request),
        device=device_info
    )