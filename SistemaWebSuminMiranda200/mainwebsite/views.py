from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import time
from .services import OrdenServ

#RECORDAR QUE ESTE ES EL WORKSPACE/ORDENES, SE DEBE CAMBIAR A FUTURO
@login_required
def home(request):
    lista_ordenes = OrdenServ.getAll()
    return render(request, 'home.html',{'ordenes':lista_ordenes})

@login_required
def orden_individual(request,pk):
    orden = OrdenServ.get()
    return render(request, 'orden')

#pagina dashboard "/workspace/"
@login_required
def ordenes(request):
    return render(request, 'workspace.html',{})

#pagina para produtos "/productos"
@login_required
def inventario(request):
    return render(request, "inventario.html",{})

@login_required
def historial_inventario(request):
    return render(request, "historial_inventario.html",{})

#pagina para proveedores "/proveedores"
@login_required
def proveedores(request):
    return render(request, "proveedores.html",{})

#pagina para clientes "/clientes"
@login_required
def clientes(request):
    return render(request, "clientes.html",{})

#pagina para clientes "/almacenes"
@login_required
def almacenes(request):
    return render(request, "almacenes.html",{})

@login_required
def almacen(request, pk):
    pass


#Inicio de sesion, si hay una sesion abierta se envia al workspace, caso contrario a la pagina de inicio
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "has iniciado sesión correctamente.")
        else:
            messages.error(request, "Usuario o contraseña incorrectos")
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'login.html', {})

#Terminar sesión
def logout_user(request):
    logout(request)
    messages.success(request, "Te has desconectado correctamente")
    return redirect('home')

#manejo de errores 404 custom
def custom_404(request, exception):
    return render(request, 'error_404.html', status=404)