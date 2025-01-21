def theme_context(request):
    THEMES = {
        'red': {
            'code_name':'red',
            'name': 'Rojo',
            'color': '#fc4103',
        },
        'blue': {
            'code_name':'blue',
            'name': 'Azul',
            'color': '#1911a6',
        },
        'grey': {
            'code_name':'grey',
            'name': 'Gris',
            'color': '#282828',
        },
        'lime': {
            'code_name':'lime',
            'name': 'Verde Lima',
            'color': '#91b41c',
        },
        'pink': {
            'code_name':'pink',
            'name': 'Rosado',
            'color': '#e758ed',
        },
        'brown': {
            'code_name':'brown',
            'name': 'Marrón',
            'color': '#522b1e',
        }
    }
    
    theme_key = 'red'  # Valor por defecto
    if request.user.is_authenticated:
        try:
            theme_key = request.user.profile.tema_sistema
        except AttributeError:
            theme_key='red'
    else:
        theme_key = request.session.get('theme', 'red')
    
    request.session['active_theme'] = theme_key
    
    return {'current_theme': THEMES[theme_key],
            'themes':THEMES.values()
            }