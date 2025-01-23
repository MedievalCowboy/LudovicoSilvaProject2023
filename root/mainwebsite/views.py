from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseNotFound, Http404, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib.auth.forms import UserCreationForm
from django.template.loader import render_to_string
from django.contrib.auth.models import User, Group
from xhtml2pdf import pisa
from django.contrib.auth import get_user_model
from django.db import transaction
from django.contrib import messages
from django.urls import reverse
from django.db.models import Count, Sum
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.contenttypes.models import ContentType
import re
import os
import csv
from django.utils import timezone
from django.templatetags.static import static
from django.contrib.admin.models import LogEntry
from django.views.decorators.cache import never_cache
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.views.generic import ListView
from .models import Almacen, Orden, Proveedor, Orden_Producto, Inventario, Producto, Destino, Prod_Dest, Cliente, Profile, LoginHistory, UserSession, AuditLog
from .forms import OrdenForm, OrdenProductoForm, InventarioForm, ProductoForm, ProveedorForm, DestinoForm, ProdDestForm, AlmacenForm, ClientesForm, CustomUserForm, ProfileForm
from .filters import LoginHistoryFilter

from .extras import send_email

from .security.utils import obtener_rol_mas_alto, puede_asignar_rol
from .security.hierarchy import HIERARCHY, get_allowed_roles, DISPLAY_NAMES
from .security.decorators import role_required, only_admin


@role_required('gerente')
def pruebas(request):
    logs = LogEntry.objects.all()
    context = {'titulo_web':'pruebabaaaa', 'log_registry':logs}
    return render(request, 'prueba1.html', context)

def portal_principal(request):
    return render(request, 'index.html', {'titulo_web':'Suministros Miranda 200 C.A'})

def mostrar_politicas(request):
    return render(request, 'politicas.html',{})

def portal_conocenos(request):
    return render(request, 'conocenos.html',{})

######################################################################################
######################################################################################
@require_POST
def set_theme(request):
    theme = request.POST.get('theme', 'red')
    if request.user.is_authenticated:
        profile = request.user.profile
        profile.tema_sistema = theme
        profile.save()
    else:
        request.session['theme'] = theme
    return redirect(request.META.get('HTTP_REFERER', '/'))


######################################################################################
######################################################################################
#SERVICIOS RELACIONADOS CON ORDENES


#pagina dashboard "workspace/ordenes/"
@login_required
def ordenes(request):
    lista_ordenes = Orden.objects.annotate(num_productos=Count('orden_producto'))
    return render(request, 'ordenes/ordenes.html',{'ordenes':lista_ordenes, 'titulo_web':'Ordenes - SM200SYS'})

@login_required
def send_orden_info_email(request, pk):
    if request.method == 'GET':
        orden = get_object_or_404(Orden, pk = pk)
        orden_productos = Orden_Producto.objects.filter(id_orden=orden)
        if re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', orden.id_cliente.correo):
            email_subject = f"Notificación de Orden #{orden.num_orden} - Suministros Miranda 200 C.A."
            text_template = "emails/order_email.txt"
            html_template = "emails/order_email.html"
            
            context = {'orden':orden,'orden_productos':orden_productos, 'contact_email':settings.EMAIL_HOST_USER , 'contact_tlf':'04265922250'}
            try:
                logo_path = static('img/sum3.png')
                logo_abs_path = f"{get_current_site(request)}{logo_path}"
                context['logo_path'] = logo_abs_path
            except Exception as e:
                pass
            email_from = settings.EMAIL_HOST_USER
            email_to = [orden.id_cliente.correo]
            if send_email(email_subject, email_from, email_to, text_template, html_template, context) == 1:
                messages.success(request, "Se envió un correo al cliente con la información de la orden.")
            else:
                print("ocurrio un error inesperado al tratar de enviar el email...")
        else:
            messages.warning(request, "Error al tratar de enviar email al cliente. El cliente no dispone de un email valido.")
    url = reverse('orden_detail', kwargs={'pk': pk})    
    return redirect(url)

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
    return render(request, 'ordenes/orden_insertar.html', {'form': form, 'titulo_web':'Insertar Orden - SM200SYS'})


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
    return render(request, 'ordenes/orden_insertar2.html', {'form': form, 'titulo_web': 'Insertar Orden - SM200SYS'})


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



#Funcion que muestra una orden en especifico.
@login_required
def orden_detail(request, pk):
    orden  = get_object_or_404(Orden, pk=pk)
    orden_productos = Orden_Producto.objects.filter(id_orden=orden)
    
    context={'orden':orden, 'orden_prod_list':orden_productos, 'titulo_web':'Vista detallada de orden', 'titulo_page':"Detalle de Orden #"+str(orden.num_orden)}

    return render(request, 'ordenes/orden_detail.html', context)


def link_callback(uri, _):
    """
    Convierte URLs estáticas a rutas del sistema.
    Ej: '/static/img/logo.png' → '/ruta/proyecto/mainwebsite/static/img/logo.png'
    """
    # Paso 1: Eliminar '/' inicial y convertir a ruta relativa
    uri = uri.lstrip('/')
    
    # Paso 2: Verificar si es una URL estática
    if uri.startswith('static/'):
        # Desarrollo: Buscar en STATICFILES_DIRS
        if settings.DEBUG:
            path = os.path.join(settings.BASE_DIR, 'mainwebsite', 'static', uri.replace('static/', ''))
        # Producción: Buscar en STATIC_ROOT
        else:
            path = os.path.join(settings.STATIC_ROOT, uri.replace('static/', ''))
        
        # Verificar si el archivo existe
        if not os.path.exists(path):
            raise ValueError(f"Archivo estático no encontrado: {path}")
        return path
    
    # Si no es estático, retornar la URI original (ej: URLs HTTP)
    return uri

def generar_pdf_orden(request, pk):
    # Obtener la orden con sus productos relacionados
    orden = Orden.objects.prefetch_related('orden_producto_set__producto').get(pk=pk)
    orden_productos = orden.orden_producto_set.all()  # Obtiene todos los productos
    
    context = {
        'orden': orden,
        'orden_productos': orden_productos, 
        'total_general': orden.get_total_general, 
        'empresa': {
            'nombre': 'Suministros Miranda 200 C.A.',
            'direccion': 'Av. Principal 123, Ciudad',
            'telefono': '0412-1234567',
            'email': 'soporte@empresa.com',
        }
    }
    
    # Renderizar plantilla HTML
    html_string = render_to_string('ordenes/pdf_orden.html', context)
    
    # Crear respuesta PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=orden_{orden.num_orden}.pdf'
    
    # Generar PDF
    pisa_status = pisa.CreatePDF(
        html_string, 
        dest=response,
        encoding='UTF-8',
        link_callback=link_callback
    )
    
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF')
    return response


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

    return render(request, 'ordenes/orden_prod_list.html', context)

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
    
    return render(request, 'ordenes/orden_prod_mod.html',context)


######################################################################################
######################################################################################

#SERVICIOS RELACIONADOS CON PRODUCTOS E INVENTARIO
@login_required
def inventario_lista(request):
    inventario_list = Inventario.objects.all()

    context = {'inventario':inventario_list,
               'titulo_web':'Inventario - SM200SYS'}
    return render(request, "inventario/inventario.html",context)

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

    return render(request, 'inventario/inventario_insertar.html', {'form': form, 'titulo_web':'Insertar Elemento en Inventario - SM200SYS'})

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
    return render(request, "inventario/productos.html", context)


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
        

    return render(request, 'inventario/producto_detail.html', context)

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

    return render(request, 'inventario/producto_insertar.html', {'form': form, 'titulo_web':'Insertar Producto - SM200SYS'})

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
    return render(request, "proveedores/proveedores.html",context)

    
@login_required
def proveedor_detail(request, pk):
    proveedor  = get_object_or_404(Proveedor, pk=pk)
    proveedor_productos = Producto.objects.filter(id_proveedor=proveedor)
    
    context={'proveedor':proveedor, 'proveedor_productos':proveedor_productos, 'titulo_web':'Vista detallada de proveedor', 'titulo_page':"Detalle del proveedor #"+str(proveedor.id_proveedor)}

    return render(request, 'proveedores/proveedor_detail.html', context)


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

    return render(request, 'proveedores/proveedor_insertar.html', {'form': form, 'titulo_web':'Insertar Proveedor - SM200SYS'})

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
    
    
    return render(request, "clientes/clientes.html",context)

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

    return render(request, 'clientes/cliente_detail.html', context)



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

    return render(request, 'clientes/cliente_insertar.html', {'form': form, 'titulo_web':'Insertar Cliente - SM200SYS'})


def cliente_modificar(request, pk):
    clientes = get_object_or_404(Cliente, pk=pk)

    if request.method == "POST":
        form = ClientesForm(request.POST,request.FILES, instance=clientes)
        if form.is_valid():
            form.save()
            messages.info(request, "Se modificó el cliente exitosamente.")
            return redirect('clientes')  

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
    return render(request, "almacenes/almacenes.html",context)

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
    

    return render(request, 'almacenes/almacen_detail.html', context)

@login_required
def almacen_modificar(request, pk):
    almacen = get_object_or_404(Almacen, pk=pk)

    if request.method == "POST":
        form = AlmacenForm(request.POST, instance=almacen)
        if form.is_valid():
            form.save()
            messages.info(request, "Se modificó el almacen exitosamente.")
            return redirect('almacenes')  

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

    return render(request, 'almacenes/almacen_insertar.html', {'form': form, 'titulo_web':'Insertar Almacen - SM200SYS'})

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
    return render(request,'destinos/destinos.html', context)

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

    return render(request, 'destinos/destino_detail.html', context)


@login_required
def destino_modificar(request, pk):
    destino = get_object_or_404(Destino, pk=pk)

    if request.method == "POST":
        form = DestinoForm(request.POST, instance=destino)
        if form.is_valid():
            form.save()
            messages.info(request, "Se modificó el destino exitosamente.")
            return redirect('destinos') 

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

    return render(request, 'destinos/destino_insertar.html', {'form': form, 'titulo_web':'Insertar Destino - SM200SYS'})

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
    
    return render(request,'inventario/prod_dest_consumos.html', context)

@login_required
def prod_dest_det_dest(request, pk):
    destino = get_object_or_404(Destino, pk=pk)
    prod_dest_det_list = Prod_Dest.objects.filter(id_destino=destino)

    context={
             'listado': prod_dest_det_list,
             'id_destino':destino.nombre_destino,
             'titulo_web':'Consumo de productos para el destino '+ destino.nombre_destino  ,}
    return render(request, 'inventario/prod_dest_det_dest.html', context)

@login_required
def prod_dest_modificar(request,pk):
    prod_dest = get_object_or_404(Prod_Dest, pk=pk)

    if request.method == "POST":
        form = ProdDestForm(request.POST, instance=prod_dest)
        if form.is_valid():
            form.save()
            messages.info(request, "Se modificó la relacion entre producto y destino exitosamente.")
            return redirect('prod_dest_lista') 

    else:
        form = ProdDestForm(instance=prod_dest)

    context = {'form': form, 
               'titulo_web': 'Modificar relación Producto en Destino - SM200SYS',
               'titulo_page':'Modificar relación Producto en Destino',
               'volver_a':'prod_dest_lista'}
    return render(request, 'inventario/prod_dest_modificar.html', context)

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
    return render(request, 'inventario/prod_dest_insertar.html', {'form': form, 'titulo_web':'Insertar relación consumo Producto/Destino - SM200SYS'})
    
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

#SERVICIOS RELACIONADOS CON USUARIOS / PERFILES DE USUARIO

@role_required('admin')  
def register_user(request):
    current_user_role = obtener_rol_mas_alto(request.user)
    allowed_roles = get_allowed_roles(current_user_role)
    
    form = CustomUserForm(request=request)
    
    if request.method == 'POST':
        form = CustomUserForm(request.POST, request=request)
        if form.is_valid():
            try:
                with transaction.atomic():
                    new_user = form.save()
                    selected_role = form.cleaned_data['rol_selector']
                    
                    if not puede_asignar_rol(current_user_role, selected_role):
                        messages.error(request, f"⛔ Rol no permitido: {DISPLAY_NAMES.get(selected_role)}")
                        return redirect('ordenes')
                    
                    group = Group.objects.get(name=selected_role)
                    new_user.groups.add(group)
                    
                    messages.success(request, f"✅ {new_user.username} creado como {DISPLAY_NAMES.get(selected_role)}")
                    return redirect('ordenes')
            
            except Group.DoesNotExist:
                messages.error(request, "❌ Error: Rol no existe en el sistema")
    
    context = {
        'form': form,
        'titulo_web': 'Crear usuario',
        'roles_permitidos': [DISPLAY_NAMES[r] for r in allowed_roles if r != 'admin']
    }
    return render(request, 'usuarios/crear_usuario.html', context)

@login_required
def user_profile(request, pk, username):
    target_user = get_object_or_404(User, pk=pk, username=username)
    current_user_role = obtener_rol_mas_alto(request.user)
    
    # Calcular si es admin
    is_admin = HIERARCHY.get(current_user_role, 0) >= HIERARCHY['admin']
    
    # Validar acceso
    if request.user == target_user or is_admin or HIERARCHY.get(current_user_role, 0) >= HIERARCHY['ceo']:
        return render_profile(request, target_user, is_admin)
    
    messages.warning(request, "No tienes permisos para ver este perfil")
    return redirect('ordenes')

def render_profile(request, user, is_admin=False):
    perfil = get_object_or_404(Profile, user=user)
    context = {
        'profile_user': user,
        'perfil': perfil,
        'titulo_web': f'Perfil de {user.username}',
        'is_admin': is_admin  # Pasar variable al template
    }
    return render(request, 'usuarios/perfil_usuario.html', context)


@login_required
def edit_profile(request, user_id=None):
    # Obtener usuario a editar
    target_user = get_object_or_404(User, pk=user_id) if user_id else request.user
    profile = get_object_or_404(Profile, user=target_user)
    
    # Verificar permisos
    current_user_role = obtener_rol_mas_alto(request.user)
    is_admin = HIERARCHY.get(current_user_role, 0) >= HIERARCHY['admin']
    
    if not (request.user == target_user or is_admin):
        messages.error(request, "No tienes permisos para editar este perfil")
        return redirect('ordenes')

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, f"Perfil de {target_user.username} actualizado")
            return redirect('user_profile', pk=target_user.pk, username=target_user.username)
    else:
        form = ProfileForm(instance=profile)
    
    # Si es admin, mostrar selector de usuario
    if is_admin:
        all_users = User.objects.all()
    else:
        all_users = None
    
    context = {
        'form': form,
        'target_user': target_user,
        'all_users': all_users,
        'titulo_web': 'Editar Perfil',
    }
    return render(request, 'usuarios/editar_perfil.html', context)

def user_list(request):
    user_list = User.objects.select_related('profile').prefetch_related('groups').all().order_by('-date_joined')
    paginator = Paginator(user_list, 25)  # 25 usuarios por página
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)
    
    context ={
        'users': users,
        'default_photo': 'static/img/profile-img.png',
        'titulo_web': 'Lista de Usuarios registrados',
    }
    
    return render(request, 'usuarios/lista_usuarios.html', context)

######################################################################################
######################################################################################

#SERVICIOS RELACIONADOS CON SESIONES DE USUARIOS

@require_http_methods(["GET", "POST"])
@never_cache
def login_user(request):
    # Redirigir usuarios ya autenticados
    if request.user.is_authenticated:
        return redirect('ordenes')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        try:
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)
                
                if user is not None:
                    login(request, user)
                    messages.success(request, f"Has iniciado sesión, {user.username}.")
                    next_url = request.POST.get('next', reverse('ordenes'))
                    return redirect(next_url)
            
            # Manejo de errores mejorado
            messages.error(request, "Credenciales inválidas. Por favor intente nuevamente.")
        
        except ValidationError as e:
            messages.error(request, f"Error de validación: {e}")
        
        except Exception as e:
            messages.error(request, "Error inesperado en el inicio de sesión")
            # Registrar el error (logging)
    
    else:
        form = AuthenticationForm()
    
    context = {
        'form': form,
        'next': request.GET.get('next', '')
    }
    return render(request, 'auth/login.html', context)

@login_required
@require_http_methods(["POST"])
@never_cache
def logout_user(request):
    try:
        username = request.user.username
        logout(request)
        messages.success(request, f"¡Hasta pronto, {username}!")
    except Exception as e:
        messages.error(request, "Error al cerrar sesión")
    
    return HttpResponseRedirect(reverse('login'))

# Listado de accesos al sistema
@login_required
@role_required('gerente')
def global_access_history(request):
    qs = LoginHistory.objects.all().order_by('-timestamp')
    
    # Aplicar filtros
    filter = LoginHistoryFilter(request.GET, queryset=qs)
    
    # Paginación
    paginator = Paginator(filter.qs, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'auth/global_history.html', {
        'filter': filter,
        'page_obj': page_obj,
        'titulo_web': 'Historial de inicios de sesión',
    })
    
## peticion para ver las sesiones de usuario activas al momento
@login_required
@role_required('gerente')
def active_sessions_view(request):
    sessions = Session.objects.filter(expire_date__gt=timezone.now())
    
    active_users = []
    for session in sessions:
        try:
            user_session = UserSession.objects.get(session_key=session.session_key)
            active_users.append(user_session)
        except UserSession.DoesNotExist:
            pass
    
    context ={
         'active_users': active_users,
        'current_user_pk': request.user.pk,
        'titulo_web': 'Usuarios activos en el sistema',
        }
    
    return render(request, 'auth/active_sessions.html', context)

## Peticion para desconectar un usuario en especifico.
@login_required
@role_required('gerente')
def disconnect_user(request, session_key):
    print("Session Key recibida:", session_key)
    try:
        # Primero verificar la sesión de Django
        try:
            
            django_session = Session.objects.get(session_key=session_key)
        except Session.DoesNotExist:
            messages.error(request, "La sesión no existe en el sistema")
            return redirect('active_sessions')
        
        # Luego verificar tu registro UserSession
        try:
            user_session = UserSession.objects.get(session_key=session_key)
        except UserSession.DoesNotExist:
            messages.error(request, "La sesión no está registrada")
            django_session.delete()  # Limpiar sesión huérfana
            return redirect('active_sessions')
        
        # Validar permisos
        if user_session.user.is_staff or user_session.user == request.user:
            messages.error(request, "Acción no permitida para este usuario")
            return redirect('active_sessions')
        
        # Eliminar en orden inverso
        with transaction.atomic():
            user_session.delete()  # Primero el registro de sesion
            django_session.delete()  # Luego la sesión de Django
            messages.success(request, f"Usuario {user_session.user.username} desconectado")
            
    except Exception as e:
        messages.error(request, "Error interno al procesar la solicitud")
    
    return redirect('active_sessions')

## Peticion para desconectar a todos los usuarios excluyendo usuarios staff 
@login_required
@role_required('gerente')
def disconnect_all(request):
    # Excluir staff y usuario actual
    sessions = UserSession.objects.exclude(
        user__is_staff=True
    ).exclude(
        user=request.user
    )
    
    count = sessions.count()
    # Eliminar sesiones
    for session in sessions:
        Session.objects.filter(session_key=session.session_key).delete()
    sessions.delete()
    
    messages.success(request, f'{count} usuarios desconectados exitosamente')
    return redirect('active_sessions')


class AuditLogListView(ListView):
    model = AuditLog
    template_name = 'auth/activity_log_list.html'
    paginate_by = 25
    context_object_name = 'logs'

    def get_queryset(self):
        qs = super().get_queryset().select_related('user', 'content_type')
        
        # Aplicar filtros simples, tal vez luego usar filtros avanzados idk
        filters = {
            'user__username__icontains': self.request.GET.get('user__username'),
            'action': self.request.GET.get('action'),
            'content_type__model': self.request.GET.get('content_type__model'),
            'ip_address': self.request.GET.get('ip_address')
        }
        
        for key, value in filters.items():
            if value:
                qs = qs.filter(**{key: value})
                
        return qs.order_by('-timestamp')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener modelos únicos para el filtro
        context['content_types'] = ContentType.objects.filter(
            pk__in=AuditLog.objects.values('content_type_id').distinct()
        )
        context['titulo_web'] = 'Historial de acciones en el sistema'
        return context

######################################################################################
######################################################################################

#manejo de errores 404 custom
def custom_404(request, exception):
    return render(request, '404.html', status=404)


def handler500(request, exception=None):
    return render(request, '500.html', status=500)
