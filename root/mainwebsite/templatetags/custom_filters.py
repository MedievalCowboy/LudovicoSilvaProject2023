from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiplica dos valores."""
    return float(value) * float(arg)

