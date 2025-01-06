from django.contrib import admin
from .models import Orden, Inventario, Proveedor, Almacen, Cliente, Destino,Orden_Producto, Producto, Prod_Dest

admin.site.register(Orden)
admin.site.register(Inventario)
admin.site.register(Proveedor)
admin.site.register(Almacen)
admin.site.register(Cliente)
admin.site.register(Destino)
admin.site.register(Orden_Producto)
admin.site.register(Producto)
admin.site.register(Prod_Dest)
