
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    path('', views.portal_principal, name="portalPrincipal"),
    path('politicas/', views.mostrar_politicas, name="politicas"),
    path('sobre_nosotros/', views.portal_conocenos, name="conocenos"),

    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='reset_password'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    
    #path('/perfil/<string:nombre>', views.perfil_usuario, name='perfil'),

    path('pruebas/', views.pruebas, name="pruebas"),

    path('workspace/ordenes/', views.ordenes, name='ordenes'),
    path('workspace/orden/<int:pk>', views.orden_detail, name="orden_detail"),
    path('workspace/orden/insertar', views.orden_insertar, name="orden_insertar"),
    path('workspace/orden/insertar-2/<int:pk>', views.orden_insertar_2, name="orden_insertar2"), #ORDEN_PROD INSERT
    path('workspace/orden/modificar/<int:pk>', views.orden_modificar, name="orden_modificar"),
    path('workspace/orden/eliminar/<int:pk>', views.orden_eliminar, name="orden_eliminar"),
    path('workspace/orden/send_email/<int:pk>', views.send_orden_info_email, name="send_orden_email"),

    path('workspace/orden_prod/listar/<int:pk>', views.orden_prod_listar, name="orden_prod_listar"),
    path('workspace/orden_prod/eliminar/<int:pk>', views.orden_prod_eliminar, name="orden_prod_eliminar"),
    path('workspace/orden_prod/modificar/<int:orden_pk>/<int:orprod_pk>', views.orden_prod_modificar, name="orden_prod_modificar"),

    path('workspace/proveedores/', views.proveedores, name='proveedores'),
    path('workspace/proveedor/<int:pk>', views.proveedor_detail, name="proveedor_detail"),
    path('workspace/proveedor/insertar', views.proveedor_insertar, name="proveedor_insertar"),
    path('workspace/proveedor/modificar/<int:pk>', views.proveedor_modificar, name="proveedor_modificar"),
    path('workspace/proveedor/eliminar/<int:pk>', views.proveedor_eliminar, name="proveedor_eliminar"),
    
    
    path('workspace/clientes/', views.clientes, name='clientes'),
    path('workspace/cliente/<int:pk>', views.cliente_detail, name="cliente_detail"),
    path('workspace/cliente/insertar', views.cliente_insertar, name="cliente_insertar"),
    path('workspace/cliente/modificar/<int:pk>', views.cliente_modificar, name="cliente_modificar"),
    path('workspace/cliente/eliminar/<int:pk>', views.cliente_eliminar, name="cliente_eliminar"),

    path('workspace/inventario/', views.inventario_lista, name='inventario'),
    path('workspace/inventario/insertar', views.inventario_insertar, name="inventario_insertar"),
    path('workspace/inventario/modificar/<int:pk>', views.inventario_modificar, name="inventario_modificar"),
    path('workspace/inventario/eliminar/<int:pk>', views.inventario_eliminar, name="inventario_eliminar"),

    path('workspace/productos/', views.producto_lista, name='productos'),
    path('workspace/producto/<int:pk>', views.producto_detail, name="producto_detail"),
    path('workspace/producto/insertar', views.producto_insertar, name="producto_insertar"),
    path('workspace/producto/modificar/<int:pk>', views.producto_modificar, name="producto_modificar"),
    path('workspace/producto/eliminar/<int:pk>', views.producto_eliminar, name="producto_eliminar"),

    path('workspace/destinos/', views.destino_lista, name='destinos'),
    path('workspace/destino/<int:pk>', views.destino_detail, name="destino_detail"),
    path('workspace/destino/insertar', views.destino_insertar, name="destino_insertar"),
    path('workspace/destino/modificar/<int:pk>', views.destino_modificar, name="destino_modificar"),
    path('workspace/destino/eliminar/<int:pk>', views.destino_eliminar, name="destino_eliminar"),

    path('workspace/destinos/consumo', views.prod_dest_lista, name='prod_dest_lista'),
    path('workspace/destino/<int:pk>/consumo', views.prod_dest_det_dest, name='prod_dest_det_dest'),
    path('workspace/destino/consumo/insertar', views.prod_dest_insertar, name="prod_dest_insertar"),
    path('workspace/destinos/consumo/modificar/<int:pk>', views.prod_dest_modificar, name='prod_dest_modificar'),
    path('workspace/destino/consumo/eliminar/<int:pk>', views.prod_dest_eliminar, name='prod_dest_eliminar'),

    path('workspace/almacenes/', views.almacenes, name='almacenes'),
    path('workspace/almacen/<int:pk>', views.almacen_detail, name="almacen_detail"),
    path('workspace/almacen/insertar', views.almacen_insertar, name="almacen_insertar"),
    path('workspace/almacen/modificar/<int:pk>', views.almacen_modificar, name="almacen_modificar"),
    path('workspace/almacen/eliminar/<int:pk>', views.almacen_eliminar, name="almacen_eliminar"),
    
]

