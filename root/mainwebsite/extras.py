import os
from datetime import datetime
import user_agents
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

#logica para enviar email a correo en formato texto y html
#Regresa 1 si se envió y 0 si no se envio nada.
def send_email(subject, from_email, to_emails, text_template, html_template, context):
    text_content = render_to_string(text_template, context = context)
    html_content = render_to_string(html_template, context = context)
    msg = EmailMultiAlternatives(subject, text_content, from_email, to_emails)
    msg.attach_alternative(html_content, "text/html")
    value = msg.send()
    return value

def generar_nombre_imagen(instance, filename, clase_modelo, campo_id, nombre_carpeta):

    ext = filename.split('.')[-1]
    if clase_modelo == 'usuario':
        new_filename = f"{clase_modelo}_{instance.user.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
    else:
        new_filename = f"{clase_modelo}_{getattr(instance, campo_id)}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
    return os.path.join('images',nombre_carpeta, new_filename)


#obtener la IP de alguien que hace una peticion.
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

#obtener user_agent del que hace una peticion
def parse_user_agent(request):
    """Analiza el User-Agent y extrae información detallada"""
    user_agent = user_agents.parse(request.META.get('HTTP_USER_AGENT', ''))
    return {
        'device_type': user_agent.device.family,
        'browser': user_agent.browser.family,
        'os': user_agent.os.family,
        'user_agent': str(user_agent)
    }
