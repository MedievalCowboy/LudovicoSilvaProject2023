from re import A
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.db.models import Count, Sum


from .models import Almacen, Orden, Proveedor, Orden_Producto, Inventario, Producto, Destino, Prod_Dest, Cliente
from .forms import OrdenForm, OrdenProductoForm, InventarioForm, ProductoForm, ProveedorForm, DestinoForm, ProdDestForm, AlmacenForm, ClientesForm

def pruebas(request):
    return render(request, 'base2.html', {'titulo_web':'pruebabaaaa'})



def portal_principal(request):
    return render(request, 'index.html', {'titulo_web':'Suministros Miranda 200 C.A'})

def mostrar_politicas(request):
    return render(request, 'politicas.html',{})

def portal_conocenos(request):
    return render(request, 'conocenos.html',{})

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
            messages.success(request, "La orden se creó exitosamente.")
            return redirect('ordenes')

        if request.POST.get('guardar_e_insertar_producto' ) and form.is_valid() :
            orden = form.save(commit=False)
            orden.id_usuario = request.user
            orden.save()
            pk_orden = orden.pk
            url = reverse('orden_insertar2', kwargs={'pk': pk_orden})
            messages.success(request, "La orden se creó exitosamente.")
            return redirect(url)
        
        if request.POST.get('guardar_y_crear_otra_orden') and form.is_valid():
            orden = form.save(commit=False)
            orden.id_usuario = request.user
            orden.save()
            messages.success(request, "La orden se creó exitosamente.")
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
            messages.success(request, "Se registró el producto a la orden exitosamente.")
            return redirect('ordenes') 

        elif request.POST.get("guardar_y_crear_otro") and form.is_valid():
            print("orden_insertar_2 CASO 2")
            form.save()
            # Limpia el formulario para crear otro
            messages.success(request, "Se registró el producto a la orden exitosamente.")
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
            messages.info(request, "Se modificó la orden exitosamente.")
            return redirect('ordenes')  # Reemplaza 'lista_ordenes' con la URL de la vista que muestra la lista de órdenes.

    else:
        form = OrdenForm(instance=orden)

    context = {'form': form, 
               'titulo_web': 'Modificar Orden - SM200SYS',
               'volver_a':'ordenes',
               'titulo_page':'Modificar Orden'}

    return render(request, 'base/base_modificar.html', context)

#Esto esta conectado con ajax
@login_required
def orden_eliminar(request, pk):
    orden = get_object_or_404(Orden, pk=pk)
    orden_productos = Orden_Producto.objects.filter(id_orden=orden)
    if request.method == 'POST':
        orden_productos.delete()
        orden.delete()
        data = {'mensaje': 'Orden eliminada exitosamente.'}
        messages.warning(request, "Se Eliminó la orden exitosamente.")
        return JsonResponse(data)
    
@login_required
def orden_detail(request, pk):
    orden  = get_object_or_404(Orden, pk=pk)
    orden_productos = Orden_Producto.objects.filter(id_orden=orden)
    
    context={'orden':orden, 'orden_prod_list':orden_productos, 'titulo_web':'Vista detallada de orden', 'titulo_page':"Detalle de Orden #"+str(orden.num_orden)}

    return render(request, 'orden_detail.html', context)


######################################################################################
######################################################################################
#SERVICIOS RELACIONADOS CON ORDEN_PRODUCTO

@login_required
def orden_prod_listar(request, pk):
    orden = get_object_or_404(Orden, pk=pk)
    orden_prod_elements = Orden_Producto.objects.filter(id_orden=orden)


    context={'id_orden':orden.id_orden,
             'num_orden': orden.num_orden, 
             'orden_prod_list': orden_prod_elements,
             'titulo_web':'Productos en la orden '+ str(orden.num_orden)  ,}

    return render(request, 'orden_prod_list.html', context)

#Esto esta conectado con ajax
@login_required
def orden_prod_eliminar(request, pk):
    orden_prod = get_object_or_404(Orden_Producto, pk=pk)
    if request.method == 'POST':
        orden_prod.delete()
        data = {'mensaje': 'Orden eliminada exitosamente.'}
        messages.warning(request, "Se Eliminó la relación del producto con la orden exitosamente.")
        return JsonResponse(data)

def orden_prod_modificar(request, orden_pk, orprod_pk):
    orden_prod = get_object_or_404(Orden_Producto, pk=orprod_pk)
    orden = get_object_or_404(Orden,pk = orden_pk)
    if request.method == 'POST':
        form = OrdenProductoForm(request.POST, instance = orden_prod)
        if form.is_valid():
            form.save()
            #ESTO NO ES SEGURO REVISARRRRRRRRRRRRRRRRRRRRRRRRRRR
            url = reverse('orden_prod_listar', kwargs={'pk': orden_pk})
            messages.info(request, "Se modificó la relación del producto con la orden exitosamente.")
            return redirect(url)
    else:
        form = OrdenProductoForm(instance = orden_prod)

    context = {'titulo_web':'Modificar Productos de Orden - SM200SYS',
               'form':form,
               'orden_id':orden_pk,
               'orden_num':orden.num_orden,
               'titulo_page':'Modificar Productos de Orden #'+str(orden.num_orden),
               }
    
    return render(request, 'orden_prod_mod.html',context)
        
    

######################################################################################
######################################################################################

#SERVICIOS RELACIONADOS CON PRODUCTOS E INVENTARIO
@login_required
def inventario_lista(request):
    inventario_list = Inventario.objects.all()

    context = {'inventario':inventario_list,
               'titulo_web':'Inventario - SM200SYS'}
    return render(request, "inventario.html",context)

@login_required
def inventario_insertar(request):
    if request.method == 'POST':
        form = InventarioForm(request.POST)
        if request.POST.get('guardar_y_regresar' )  and form.is_valid() :
            inv_element = form.save(commit=False)
            inv_element.save()
            messages.success(request, "El inventario se añadío exitosamente.")
            return redirect('inventario')
        
        if request.POST.get('guardar_y_crear_otro') and form.is_valid():
            inv_element = form.save(commit=False)
            inv_element.save()
            messages.success(request, "El inventario se añadío exitosamente.")
            form = InventarioForm()
            
    else:
        form = InventarioForm()

    return render(request, 'inventario_insertar.html', {'form': form, 'titulo_web':'Insertar Elemento en Inventario - SM200SYS'})

@login_required
def inventario_modificar(request, pk):
    inv_element = get_object_or_404(Inventario, pk=pk)

    if request.method == "POST":
        form = InventarioForm(request.POST, instance=inv_element)
        if form.is_valid():
            form.save()
            messages.info(request, "Se modificó el elemento de inventario con exito.")
            return redirect('inventario')  # Reemplaza 'lista_ordenes' con la URL de la vista que muestra la lista de órdenes.

    else:
        form = InventarioForm(instance=inv_element)

    context= {'form': form, 
              'titulo_web': 'Modificar Elemento en Inventario - SM200SYS',
              'titulo_page':'Modificar elemento de inventario',
              'volver_a':'inventario'}
    return render(request, 'base/base_modificar.html', context)


@login_required
def inventario_eliminar(request, pk):
    inv_element = get_object_or_404(Inventario, pk=pk)
    if request.method == 'POST':
        inv_element.delete()
        data = {'mensaje': 'Elemento de inventario eliminado exitosamente.'}
        messages.warning(request, "Se Eliminó el elemento de inventario exitosamente.")
        return JsonResponse(data)



@login_required
def producto_lista(request):
    producto_list = Producto.objects.all()

    context = {'productos':producto_list,
               'titulo_web':"Productos - SM200SYS",}
    return render(request, "productos.html", context)


@login_required
def producto_detail(request, pk):
    producto  = get_object_or_404(Producto, pk=pk)

    context={'producto':producto,
             'titulo_web':'Vista detallada de producto', 
             'titulo_page':"Detalle del producto #"+str(producto.id_producto)
             }

    try:
        prod_inv = get_object_or_404(Inventario, producto = producto)
        context['inventario'] = prod_inv
    except Exception as e:
        pass
        

    return render(request, 'producto_detail.html', context)

@login_required
def producto_insertar(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if request.POST.get('guardar_y_regresar' )  and form.is_valid():

            producto = form.save(commit=False)
            producto.save()
            messages.success(request, "El producto se creó exitosamente.")
            return redirect('productos')
        
        if request.POST.get('guardar_y_crear_otro_producto') and form.is_valid():
            producto = form.save(commit=False)
            producto.save()
            messages.success(request, "El producto se creó exitosamente.")
            form = ProductoForm()
            
    else:
        form = ProductoForm()

    return render(request, 'producto_insertar.html', {'form': form, 'titulo_web':'Insertar Producto - SM200SYS'})

@login_required
def producto_modificar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.info(request, "Se modificó el producto exitosamente.")
            return redirect('productos')  # Reemplaza 'lista_ordenes' con la URL de la vista que muestra la lista de órdenes.

    else:
        form = ProductoForm(instance=producto)

    context= {'form': form, 
              'titulo_web': 'Modificar Producto - SM200SYS',
              'titulo_page':'Modificar Producto',
              'volver_a':'productos'}
    return render(request, 'base/base_modificar.html', context)

@login_required
def producto_eliminar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        data = {'mensaje': 'Producto eliminado exitosamente.'}
        messages.warning(request, "Se Eliminó el producto exitosamente.")
        return JsonResponse(data)

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
def proveedor_detail(request, pk):
    proveedor  = get_object_or_404(Proveedor, pk=pk)
    proveedor_productos = Producto.objects.filter(id_proveedor=proveedor)
    
    context={'proveedor':proveedor, 'proveedor_productos':proveedor_productos, 'titulo_web':'Vista detallada de proveedor', 'titulo_page':"Detalle del proveedor #"+str(proveedor.id_proveedor)}

    return render(request, 'proveedor_detail.html', context)


@login_required
def proveedor_modificar(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)

    if request.method == "POST":
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.info(request, "Se modificó el proveedor exitosamente.")
            return redirect('proveedores')  # Reemplaza 'lista_ordenes' con la URL de la vista que muestra la lista de órdenes.

    else:
        form = ProveedorForm(instance=proveedor)

    context = {'form': form, 
               'titulo_web': 'Modificar Proveedor - SM200SYS',
               'titulo_page':'Modificar Proveedor',
               'volver_a':'proveedores'}
    return render(request, 'base/base_modificar.html', context)

@login_required
def proveedor_insertar(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if request.POST.get('guardar_y_regresar' )  and form.is_valid() :
            proveedor = form.save(commit=False)
            proveedor.save()
            messages.success(request, "El proveedor se creó exitosamente.")
            return redirect('proveedores')
        
        if request.POST.get('guardar_y_crear_otro') and form.is_valid():
            proveedor = form.save(commit=False)
            proveedor.save()
            messages.success(request, "El proveedor se creó exitosamente.")
            form = ProveedorForm()
            
    else:
        form = ProveedorForm()

    return render(request, 'proveedor_insertar.html', {'form': form, 'titulo_web':'Insertar Proveedor - SM200SYS'})

@login_required
def proveedor_eliminar(request, pk):
    if request.method == 'POST':
        proveedor = get_object_or_404(Proveedor, pk=pk)
        proveedor.delete()
        data = {'mensaje': 'Proveedor eliminado exitosamente.'}

        messages.warning(request, "Se eliminó el proveedor exitosamente.")
        return JsonResponse(data)
    

######################################################################################
######################################################################################

#SERVICIOS RELACIONADOS CON CLIENTES
@login_required
def clientes(request):
    # lista_ordenes = Orden.objects.annotate(num_productos=Count('orden_producto'))
    clientes_lista = Cliente.objects.annotate(num_ordenes=Count('orden'))
    
    context = {'clientes':clientes_lista,
               'titulo_web':'Clientes - SM200SYS'}
    
    
    return render(request, "clientes.html",context)

@login_required
def cliente_detail(request, pk):
    cliente  = get_object_or_404(Cliente, pk=pk)
    
    context={'cliente':cliente,  
             'titulo_web':'Vista detallada de cliente', 
             'titulo_page':"Detalle del cliente #"+str(cliente.id_cliente)}
    
    try:
        cliente_ordenes = get_list_or_404(Orden, id_cliente = cliente)
        context['cliente_ordenes'] = cliente_ordenes
    except Exception as e:
        pass

    return render(request, 'cliente_detail.html', context)



def cliente_insertar(request):
    if request.method == 'POST':

        form = ClientesForm(request.POST,request.FILES)
        if request.POST.get('guardar_y_regresar' )  and form.is_valid() :
            clientes = form.save(commit=False)
            clientes.save()
            messages.success(request, "El cliente se agrego exitosamente.")
            return redirect('clientes')
        
        if request.POST.get('guardar_y_crear_otro') and form.is_valid():
            clientes = form.save(commit=False)
            clientes.save()
            messages.success(request, "El cliente se agrego exitosamente.")
            form = ProveedorForm()
            
    else:
        form = ClientesForm()

    return render(request, 'cliente_insertar.html', {'form': form, 'titulo_web':'Insertar Cliente - SM200SYS'})


def cliente_modificar(request, pk):
    clientes = get_object_or_404(Cliente, pk=pk)

    if request.method == "POST":
        form = ClientesForm(request.POST,request.FILES, instance=clientes)
        if form.is_valid():
            form.save()
            messages.info(request, "Se modificó el cliente exitosamente.")
            return redirect('clientes')  # Reemplaza 'lista_ordenes' con la URL de la vista que muestra la lista de órdenes.

    else:
        form = ClientesForm(instance=clientes)

    context = {'form': form, 
               'titulo_web': 'Modificar Cliente - SM200SYS',
               'titulo_page':'Modificar Cliente',
               'volver_a':'clientes'}
    return render(request, 'base/base_modificar.html', context)

def cliente_eliminar(request,pk):
    clientes = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        clientes.delete()
        data = {'mensaje': 'Cliente eliminado exitosamente.'}
        messages.warning(request, "Se Eliminó el cliente exitosamente.")
        return JsonResponse(data)




######################################################################################
######################################################################################


#SERVICIOS RELACIONADOS CON ALMACEN
@login_required
def almacenes(request):
    almacenes_lista = Almacen.objects.all()

    for almacen in almacenes_lista:
        almacen.conteo_productos = almacen.inventario_set.aggregate(total=Sum('cant_disponible'))['total'] or 0
    
    context = {'almacenes':almacenes_lista,
               'titulo_web':'Almacenes - SM200SYS'}
    return render(request, "almacenes.html",context)

@login_required
def almacen_detail(request, pk):
    almacen  = get_object_or_404(Almacen, pk=pk)
    try:
        almacen.conteo_productos = almacen.inventario_set.aggregate(total=Sum('cant_disponible'))['total'] or 0
    except Exception as e:
        pass
    
    context={'almacen':almacen,  
             'titulo_web':'Vista detallada de almacen', 
             'titulo_page':"Detalle del almacen #"+str(almacen.id_almacen)}
    

    return render(request, 'almacen_detail.html', context)

@login_required
def almacen_modificar(request, pk):
    almacen = get_object_or_404(Almacen, pk=pk)

    if request.method == "POST":
        form = AlmacenForm(request.POST, instance=almacen)
        if form.is_valid():
            form.save()
            messages.info(request, "Se modificó el almacen exitosamente.")
            return redirect('almacenes')  # Reemplaza 'lista_ordenes' con la URL de la vista que muestra la lista de órdenes.

    else:
        form = AlmacenForm(instance=almacen)

    context = {'form': form, 
               'titulo_web': 'Modificar Almacen - SM200SYS',
               'titulo_page':'Modificar Almacen',
               'volver_a':'almacenes'}
    return render(request, 'base/base_modificar.html', context)

@login_required
def almacen_insertar(request):
    if request.method == 'POST':
        form = AlmacenForm(request.POST)
        if request.POST.get('guardar_y_regresar' )  and form.is_valid() :
            almacen = form.save(commit=False)
            almacen.save()
            messages.success(request, "El almacen se creó exitosamente.")
            return redirect('almacenes')
        
        if request.POST.get('guardar_y_crear_otro') and form.is_valid():
            almacen = form.save(commit=False)
            almacen.save()
            messages.success(request, "El almacen se creó exitosamente.")
            form = AlmacenForm()
    else: 
        form = AlmacenForm()

    return render(request, 'almacen_insertar.html', {'form': form, 'titulo_web':'Insertar Almacen - SM200SYS'})

@login_required
def almacen_eliminar(request, pk):
    if request.method == 'POST':
        almacen = get_object_or_404(Almacen, pk=pk)
        almacen.delete()
        data = {'mensaje': 'Almacen eliminado exitosamente.'}
        messages.warning(request, "Se eliminó el almacen exitosamente.")
        return JsonResponse(data)

######################################################################################
######################################################################################

#SERVICIOS RELACIONADOS CON DESTINOS

@login_required
def destino_lista(request):
    destinos = Destino.objects.annotate(orden_count=Count('orden'))
    context = {
        'destinos': destinos,
        'titulo_web':'Destinos - SM200SYS'
    }
    return render(request,'destinos.html', context)

@login_required
def destino_detail(request, pk):
    destino  = get_object_or_404(Destino, pk=pk)
    
    context={'destino':destino,  
             'titulo_web':'Vista detallada de destino', 
             'titulo_page':"Detalle del destino #"+str(destino.id_destino)}
    
    try:
        destino_ordenes = get_list_or_404(Orden, id_destino = destino)
        context['destino_ordenes'] = destino_ordenes
    except Exception as e:
        pass

    return render(request, 'destino_detail.html', context)


@login_required
def destino_modificar(request, pk):
    destino = get_object_or_404(Destino, pk=pk)

    if request.method == "POST":
        form = DestinoForm(request.POST, instance=destino)
        if form.is_valid():
            form.save()
            messages.info(request, "Se modificó el destino exitosamente.")
            return redirect('destinos')  # Reemplaza 'lista_ordenes' con la URL de la vista que muestra la lista de órdenes.

    else:
        form = DestinoForm(instance=destino)

    context = {'form': form, 
               'titulo_web': 'Modificar Destino - SM200SYS',
               'titulo_page':'Modificar Destino',
               'volver_a':'destinos'}
    return render(request, 'base/base_modificar.html', context)

@login_required
def destino_insertar(request):
    if request.method == 'POST':
        form = DestinoForm(request.POST)
        if request.POST.get('guardar_y_regresar' )  and form.is_valid() :
            destino = form.save(commit=False)
            destino.save()
            messages.success(request, "El destino se creó exitosamente.")
            return redirect('destinos')
        
        if request.POST.get('guardar_y_crear_otro') and form.is_valid():
            destino = form.save(commit=False)
            destino.save()
            messages.success(request, "El destino se creó exitosamente.")
            form = DestinoForm()
            
    else:
        form = DestinoForm()

    return render(request, 'destino_insertar.html', {'form': form, 'titulo_web':'Insertar Destino - SM200SYS'})

@login_required
def destino_eliminar(request, pk):
    if request.method == 'POST':
        destino = get_object_or_404(Destino, pk=pk)
        destino.delete()
        data = {'mensaje': 'Destino eliminado exitosamente.'}
        messages.warning(request, "Se eliminó el destino exitosamente.")
        return JsonResponse(data)


#SERVICIOS RELACIONADOS CON PRODUCTOS x DESTINOS

@login_required
def prod_dest_lista(request):
    prod_dest_list = Prod_Dest.objects.all()

    context = {'consumos':prod_dest_list,
               'titulo_web':'Consumo general de Productos/Destinos - SM200SYS'}
    
    return render(request,'prod_dest_consumos.html', context)

@login_required
def prod_dest_det_dest(request, pk):
    destino = get_object_or_404(Destino, pk=pk)
    prod_dest_det_list = Prod_Dest.objects.filter(id_destino=destino)

    context={
             'listado': prod_dest_det_list,
             'id_destino':destino.nombre_destino,
             'titulo_web':'Consumo de productos para el destino '+ destino.nombre_destino  ,}
    return render(request, 'prod_dest_det_dest.html', context)

@login_required
def prod_dest_modificar(request,pk):
    prod_dest = get_object_or_404(Prod_Dest, pk=pk)

    if request.method == "POST":
        form = ProdDestForm(request.POST, instance=prod_dest)
        if form.is_valid():
            form.save()
            messages.info(request, "Se modificó la relacion entre producto y destino exitosamente.")
            return redirect('prod_dest_lista')  # Reemplaza 'lista_ordenes' con la URL de la vista que muestra la lista de órdenes.

    else:
        form = ProdDestForm(instance=prod_dest)

    context = {'form': form, 
               'titulo_web': 'Modificar relación Producto en Destino - SM200SYS',
               'titulo_page':'Modificar relación Producto en Destino',
               'volver_a':'prod_dest_lista'}
    return render(request, 'prod_dest_modificar.html', context)

@login_required
def prod_dest_insertar(request):
    if request.method == 'POST':
        form = ProdDestForm(request.POST)
        if request.POST.get('guardar_y_regresar' )  and form.is_valid() :
            prod_dest = form.save(commit=False)
            prod_dest.save()
            messages.success(request, "La relación de consumo producto/destino se creó exitosamente.")
            return redirect('prod_dest_lista')
        
        if request.POST.get('guardar_y_crear_otro') and form.is_valid():
            prod_dest = form.save(commit=False)
            prod_dest.save()
            messages.success(request, "La relación de consumo producto/destino se creó exitosamente.")
            form = ProdDestForm()
            
    else:
        form = ProdDestForm()

    print("llego")
    return render(request, 'prod_dest_insertar.html', {'form': form, 'titulo_web':'Insertar relación consumo Producto/Destino - SM200SYS'})
    
@login_required
def prod_dest_eliminar(request, pk):
    if request.method == 'POST':
        prod_dest = get_object_or_404(Prod_Dest, pk=pk)
        prod_dest.delete()
        data = {'mensaje': 'Relación producto destino eliminada exitosamente.'}
        messages.warning(request, "Relación producto destino eliminada exitosamente.")
        return JsonResponse(data)


######################################################################################
######################################################################################

#SERVICIOS RELACIONADOS CON SESIONES DE USUARIOS
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Has iniciado sesión correctamente.")
        else:
            messages.warning(request, "Usuario o contraseña incorrectos.")
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

