from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .models import Almacen, Orden, Proveedor, Orden_Producto
from django.db.models import Count


from .forms import OrdenForm, OrdenProductoForm

def portal_principal(request):
    return render(request, 'index.html', {'titulo_web':'Suministros Miranda 200 C.A'})



######################################################################################
######################################################################################
#SERVICIOS RELACIONADOS CON ORDENES

#pagina dashboard "workspace/ordenes/"
@login_required
def ordenes(request):
    lista_ordenes = Orden.objects.annotate(num_productos=Count('orden_producto'))
    return render(request, 'ordenes.html',{'ordenes':lista_ordenes, 'titulo_web':'Ordenes - SM200SYS'})

@login_required
def orden_insertar(request):
    if request.method == 'POST':
        form = OrdenForm(request.POST)
        if request.POST.get('guardar_y_regresar' )  and form.is_valid() :
            orden = form.save(commit=False)
            orden.id_usuario = request.user
            orden.save()
            return redirect('ordenes')

        if request.POST.get('guardar_e_insertar_producto' ) and form.is_valid() :
            orden = form.save(commit=False)
            orden.id_usuario = request.user
            orden.save()
            pk_orden = orden.pk
            url = reverse('orden_insertar2', kwargs={'pk': pk_orden})
            return redirect(url)
        
        if request.POST.get('guardar_y_crear_otra_orden') and form.is_valid():
            orden = form.save(commit=False)
            orden.id_usuario = request.user
            orden.save()
            form = OrdenForm()
            
    else:
        form = OrdenForm()

    return render(request, 'orden_insertar.html', {'form': form, 'titulo_web':'Insertar Orden - SM200SYS'})


@login_required
def orden_insertar_2(request, pk):
    if request.method == 'POST':
        form = OrdenProductoForm(request.POST, pk=pk)

        if request.POST.get("guardar_y_regresar") and form.is_valid():
            print("orden_insertar_2 CASO 1")
            form.save()
            return redirect('ordenes') 

        elif request.POST.get("guardar_y_crear_otro") and form.is_valid():
            print("orden_insertar_2 CASO 2")
            form.save()
            # Limpia el formulario para crear otro
            form = OrdenProductoForm(pk=pk)

    else:
        form = OrdenProductoForm(pk=pk)

    return render(request, 'orden_insertar2.html', {'form': form, 'titulo_web': 'Insertar Orden - SM200SYS'})


@login_required
def orden_modificar(request,pk):
    orden = get_object_or_404(Orden, pk=pk)

    if request.method == "POST":
        form = OrdenForm(request.POST, instance=orden)
        if form.is_valid():
            form.save()
            return redirect('ordenes')  # Reemplaza 'lista_ordenes' con la URL de la vista que muestra la lista de órdenes.
    else:
        form = OrdenForm(instance=orden)

    return render(request, 'orden_modificar.html', {'form': form, 'titulo_web': 'Modificar Orden - SM200SYS'})

@login_required
def orden_eliminar(request, pk):
    orden = get_object_or_404(Orden, pk=pk)
    orden_productos = Orden_Producto.objects.filter(id_orden=orden)
    if request.method == 'POST':
        orden_productos.delete()
        orden.delete()
        data = {'mensaje': 'Orden eliminada exitosamente.'}
        return JsonResponse(data)


#Orden_Producto relacionados

@login_required
def orden_prod_listar(request, pk):
    orden = get_object_or_404(Orden, pk=pk)
    orden_prod_elements = Orden_Producto.objects.filter(id_orden=orden)

    return render(request, 'orden_prod_list.html', {'id_orden':orden.id_orden,'num_orden': orden.num_orden, 'orden_prod_list': orden_prod_elements})

@login_required
def orden_prod_eliminar(request, pk):
    orden_prod = get_object_or_404(Orden_Producto, pk=pk)
    if request.method == 'POST':
        orden_prod.delete()
        data = {'mensaje': 'Orden eliminada exitosamente.'}
        return JsonResponse(data)

def orden_prod_modificar(request, pk):
    pass

######################################################################################
######################################################################################

#SERVICIOS RELACIONADOS CON PRODUCTOS E INVENTARIO
@login_required
def inventario(request):
    return render(request, "inventario.html",{})



@login_required
def historial_inventario(request):
    return render(request, "historial_inventario.html",{})

######################################################################################
######################################################################################

#SERVICIOS RELACIONADOS CON PROVEEDOR
@login_required
def proveedores(request):
    proveedores_lista = Proveedor.objects.all()
    total_lista = len(proveedores_lista)
    context = {'proveedores':proveedores_lista,
               'total': total_lista,}
    return render(request, "proveedores.html",context)

@login_required
def proveedor_modificar(request, pk):
    proveedor = Proveedor.objects.get(pk=pk)
    data = {
        'id': proveedor.id_proveedor,
        'nombre': proveedor.nombre_proveedor,
        'correo': proveedor.correo,
        'tlf': proveedor.tlf_proveedor,
        'nota': proveedor.nota_proveedor,
    }
    return JsonResponse(data)

@login_required
def proveedor_insertar(request):
    if request.method == 'POST':
        id_proveedor = request.POST.get('id_proveedor')
        nombre_proveedor = request.POST.get('nombre_proveedor')
        correo = request.POST.get('correo_proveedor')
        tlf_proveedor = request.POST.get('tlf_proveedor')
        nota_proveedor= request.POST.get('nota_proveedor')

        if id_proveedor:
            proveedor = Proveedor.objects.get(pk=id_proveedor)
            proveedor.nombre_proveedor = nombre_proveedor
            proveedor.correo = correo
            proveedor.tlf_proveedor = tlf_proveedor
            proveedor.nota_proveedor = nota_proveedor
            proveedor.save()
        else:
            proveedor = Proveedor.objects.create(nombre_proveedor=nombre_proveedor,
                                                 correo=correo,
                                                 tlf_proveedor=tlf_proveedor,
                                                 nota_proveedor=nota_proveedor)
        data = {'mensaje': 'Proveedor guardado exitosamente.'}
        return JsonResponse(data)

@login_required
def proveedor_eliminar(request, pk):
    if request.method == 'POST':
        proveedor = get_object_or_404(Proveedor, pk=pk)
        proveedor.delete()
        data = {'mensaje': 'Proveedor eliminado exitosamente.'}
        return JsonResponse(data)
    
######################################################################################
######################################################################################

#SERVICIOS RELACIONADOS CON CLIENTES
@login_required
def clientes(request):
    return render(request, "clientes.html",{})

######################################################################################
######################################################################################


#SERVICIOS RELACIONADOS CON ALMACEN
@login_required
def almacenes(request):
    almacenes_lista = Almacen.objects.all()
    total_lista = len(almacenes_lista)
    context = {'almacenes':almacenes_lista,
               'total': total_lista,}
    return render(request, "almacenes.html",context)

@login_required
def almacen_modificar(request, pk):
    almacen = Almacen.objects.get(pk=pk)
    data = {
        'id': almacen.id_almacen,
        'nombre': almacen.nombre_almacen
    }
    return JsonResponse(data)

@login_required
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

@login_required
def almacen_eliminar(request, pk):
    if request.method == 'POST':
        almacen = get_object_or_404(Almacen, pk=pk)
        almacen.delete()
        data = {'mensaje': 'Almacen eliminado exitosamente.'}
        return JsonResponse(data)

######################################################################################
######################################################################################

#SERVICIOS RELACIONADOS CON SESIONES DE USUARIOS
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
        return redirect('ordenes')
    return render(request, 'login.html', {})

#Terminar sesión
def logout_user(request):
    logout(request)
    messages.success(request, "Te has desconectado correctamente")
    #return redirect('ordenes')
    return HttpResponseRedirect(reverse('login')) 

######################################################################################
######################################################################################

#manejo de errores 404 custom
def custom_404(request, exception):
    return render(request, 'error_404.html', status=404)

