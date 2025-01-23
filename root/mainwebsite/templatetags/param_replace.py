from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    """
    Mantiene los parámetros GET existentes mientras actualiza los especificados.
    """
    request = context.get('request')
    if not request:
        return ''
    
    params = request.GET.copy()
    
    # Actualiza con los nuevos parámetros
    for key, value in kwargs.items():
        if value is not None and value != '':
            params[key] = value
        else:
            params.pop(key, None)  # Elimina si el valor es None o vacío
    
    # Elimina parámetros vacíos
    for key in list(params.keys()):
        if not params[key]:
            del params[key]
    
    return params.urlencode()