from django import template
from django.contrib.auth.models import Group 

from ..extras import obtener_rol_mas_alto

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name): 
    group = Group.objects.get(name=group_name) 
    return True if group in user.groups.all() else False

@register.filter(name="higher_group")
def higher_group(user):
    group = obtener_rol_mas_alto(user)
    return group