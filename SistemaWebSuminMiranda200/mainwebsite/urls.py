
from django.urls import path
from . import views

urlpatterns = [
    path('workspace', views.home, name="home"),

    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    
    #path('/perfil/<string:nombre>', views.perfil_usuario, name='perfil'),

    path('workspace/ordenes/', views.ordenes, name='ordenes'),
    path('workspace/orden/<int:pk>', views.orden_individual, name="ordenIndividual"),
    #path('workspace/ordenes/insertar', views.ordenes_insertar, name="ordenes_insertar"),
    #path('workspace/ordenes/modificar/%id%', views.ordenes_modificar, name="ordenes_modificar"),
    #path('workspace/ordenes/eliminar/%id%', views.ordenes_eliminar, name="ordenes_eliminar"),

    path('workspace/proveedores/', views.proveedores, name='proveedores'),
    #path('workspace/proveedores/insertar', views.proveedores_insertar, name="proveedores_insertar"),
    #path('workspace/proveedores/modificar/%id%', views.proveedores_modificar, name="proveedores_modificar"),
    #path('workspace/proveedores/eliminar/%id%', views.proveedores_eliminar, name="proveedores_eliminar"),
    
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
    #path('workspace/almacen/<int:pk>', views.almacen_individual, name='almacenIndividual'),
    path('workspace/almacen/insertar', views.almacen_insertar, name="almacen_insertar"),
    path('workspace/almacen/modificar/<int:pk>', views.almacen_modificar, name="almacen_modificar"),
    path('workspace/almacen/eliminar/<int:pk>', views.almacen_eliminar, name="almacen_eliminar"),
    
]

