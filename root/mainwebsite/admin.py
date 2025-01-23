from django.contrib import admin
from .models import Orden, Inventario, Profile, Proveedor, Almacen, Cliente, Destino,Orden_Producto, Producto, Prod_Dest, LoginHistory

from django.utils.html import format_html

admin.site.register(Orden)
admin.site.register(Inventario)
admin.site.register(Proveedor)
admin.site.register(Almacen)
admin.site.register(Cliente)
admin.site.register(Destino)
admin.site.register(Orden_Producto)
admin.site.register(Producto)
admin.site.register(Prod_Dest)
admin.site.register(Profile)


@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'event_type', 'timestamp', 'ip_address', 'device_info')
    list_filter = ('event_type', 'timestamp', 'device_type', 'operating_system')
    search_fields = ('user__username', 'ip_address', 'user_agent')
    readonly_fields = ('timestamp',)
    date_hierarchy = 'timestamp'

    def device_info(self, obj):
        return format_html(
            "{}<br>{}<br>{}",
            obj.device_type,
            obj.operating_system,
            obj.browser
        )
    device_info.short_description = 'Dispositivo'

