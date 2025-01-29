from django import template
from datetime import timedelta

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiplica dos valores."""
    return float(value) * float(arg)

@register.filter
def add_days(fecha, days):
    try:
        return fecha + timedelta(days=int(days))
    except:
        return fecha