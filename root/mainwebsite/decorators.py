from django.shortcuts import redirect

#DECORATORS QUE LIMITAN EL ACCESO A PETICIONES DEPENDIENDO DE RANGO O GRUPO DE USUARIO

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            if request.user.groups.exists():
                groups = request.user.groups.all()
                for group in groups:
                    if group.name in allowed_roles:
                        return view_func(request, *args, *kwargs)
                return redirect('ordenes')
            return redirect('ordenes')

        return wrapper_func
    return decorator

def only_admin(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.is_staff:
                return view_func(request, *args, *kwargs)
            return redirect('ordenes')

        return wrapper_func