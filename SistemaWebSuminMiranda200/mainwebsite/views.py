from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import time
from .services import OrdenServ
from .models import Almacen

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
    almacenes_lista = Almacen.objects.all()
    total_lista = len(almacenes_lista)
    context = {'almacenes':almacenes_lista,
               'total': total_lista,}
    return render(request, "almacenes.html",context)

#@login_required
#def almacen_individual(request, pk):
#    almacen_record = Almacen.objects.get(id_almacen=pk)
#    context = {'almacen':almacen_record}
#   return render(request,"almacen.html", context)

def almacen_modificar(request, pk):
    almacen = get_object_or_404(Almacen, pk=pk)
    data = {
        'id': almacen.id_almacen,
        'nombre': almacen.nombre_almacen
    }
    return JsonResponse(data)

def almacen_insertar(request):
    if request.method == 'POST':
        id_almacen = request.POST.get('id_almacen')
        nombre_almacen = request.POST.get('nombre_almacen')
        if id_almacen:
            almacen = Almacen.objects.get(pk=id_almacen)
            almacen.nombre_almacen = nombre_almacen
            almacen.save()
        else:
            almacen = Almacen.objects.create(nombre_almacen=nombre_almacen)
        data = {'mensaje': 'Almacen guardado exitosamente.'}
        return JsonResponse(data)

def almacen_eliminar(request, pk):
    if request.method == 'POST':
        almacen = get_object_or_404(Almacen, pk=pk)
        almacen.delete()
        data = {'mensaje': 'Almacen eliminado exitosamente.'}
        return JsonResponse(data)


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