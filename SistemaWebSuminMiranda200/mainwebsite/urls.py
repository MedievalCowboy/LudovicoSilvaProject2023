
from django.urls import path
from . import views

urlpatterns = [

    path('', views.portal_principal, name="portalPrincipal"),

    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    
    #path('/perfil/<string:nombre>', views.perfil_usuario, name='perfil'),

    path('workspace/ordenes/', views.ordenes, name='ordenes'),
    path('workspace/orden/insertar', views.orden_insertar, name="orden_insertar"),
    path('workspace/orden/insertar-2/<int:pk>', views.orden_insertar_2, name="orden_insertar2"), #ORDEN_PROD INSERT
    path('workspace/orden/modificar/<int:pk>', views.orden_modificar, name="orden_modificar"),
    path('workspace/orden/eliminar/<int:pk>', views.orden_eliminar, name="orden_eliminar"),

    path('workspace/orden_prod/listar/<int:pk>', views.orden_prod_listar, name="orden_prod_listar"),
    path('workspace/orden_prod/eliminar/<int:pk>', views.orden_prod_eliminar, name="orden_prod_eliminar"),
    path('workspace/orden_prod/modificar/<int:pk>', views.orden_prod_modificar, name="orden_prod_modificar"),

    path('workspace/proveedores/', views.proveedores, name='proveedores'),
    path('workspace/proveedor/insertar', views.proveedor_insertar, name="proveedor_insertar"),
    path('workspace/proveedor/modificar/<int:pk>', views.proveedor_modificar, name="proveedor_modificar"),
    path('workspace/proveedor/eliminar/<int:pk>', views.proveedor_eliminar, name="proveedor_eliminar"),
    
    path('workspace/clientes/', views.clientes, name='clientes'),
    #path('workspace/clientes/insertar', views.clientes_insertar, name="clientes_insertar"),
    #path('workspace/clientes/modificar/%id%', views.clientes_modificar, name="clientes_modificar"),
    #path('workspace/clientes/eliminar/%id%', views.clientes_eliminar, name="clientes_eliminar"),

    path('workspace/inventario/', views.inventario, name='inventario'),
    #path('workspace/inventario/insertar', views.inventario_insertar, name="inventario_insertar"),
    #path('workspace/inventario/modificar/%id%', views.inventario_modificar, name="inventario_modificar"),
    #path('workspace/inventario/eliminar/%id%', views.inventario_eliminar, name="inventario_eliminar"),

    path('workspace/inventario/historial', views.historial_inventario, name="historial_inventario"),

    path('workspace/almacenes/', views.almacenes, name='almacenes'),
    path('workspace/almacen/insertar', views.almacen_insertar, name="almacen_insertar"),
    path('workspace/almacen/modificar/<int:pk>', views.almacen_modificar, name="almacen_modificar"),
    path('workspace/almacen/eliminar/<int:pk>', views.almacen_eliminar, name="almacen_eliminar"),
    
]

