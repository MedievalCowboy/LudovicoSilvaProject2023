from django.db import models
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext as _
from .extras import generar_nombre_imagen

def generar_nombre_imgen_cliente(instance, filename):
    return generar_nombre_imagen(instance, filename, 'cliente', 'id_cliente', 'clients')

def generar_nombre_imgen_producto(instance, filename):
    return generar_nombre_imagen(instance, filename, 'producto', 'id_producto', 'products')

def generar_nombre_imgen_usuario(instance, filename):
    return generar_nombre_imagen(instance, filename, 'usuario', 'id', 'usuarios')

TEMAS_SISTEMA = [
    ('red', 'Rojo'),
    ('blue', 'Azul'),
    ('grey','Gris'),
    ('lime', 'Lima'),
    ('pink', 'Rosado'),
    ('brown', "Marrón"),
]

LOGIN_CHOICES =[
    ('login', 'Inicio de Sesión'),
    ('logout', 'Cerrar sesión'),
    ('failed_attempt', 'Intento Fallido'),
]

class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40, unique=True)
    login_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    device = models.CharField(max_length=255)
    last_activity = models.DateTimeField(auto_now=True)

    @property
    def is_active(self):
        return Session.objects.filter(
            session_key=self.session_key,
            expire_date__gt=timezone.now()
        ).exists()

class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=20, choices=LOGIN_CHOICES)
    timestamp = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255)
    device_type = models.CharField(max_length=50, blank=True)
    browser = models.CharField(max_length=50, blank=True)
    operating_system = models.CharField(max_length=50, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Historial de Acceso'
        verbose_name_plural = 'Historial de accesos'
    def __str__(self):
        return f"{self.user.username} - {self.event_type} - {self.timestamp}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    nombres = models.CharField(max_length=200, null=True, blank=True)
    apellidos = models.CharField(max_length=200, null=True, blank=True)
    telefono = models.CharField(max_length=12, null=True, blank=True)
    telefono2 = models.CharField(max_length=12, blank=True, null=True)
    cedula = models.CharField(max_length=12, blank=True, null=True)
    email = models.CharField(max_length=150, blank=True, null=True)
    estado = models.CharField(max_length=40, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    cargo = models.CharField(max_length=200, null=True, blank=True)
    tema_sistema = models.CharField(max_length=20,choices=TEMAS_SISTEMA, default='red')
    image = models.ImageField(blank=True, upload_to=generar_nombre_imgen_usuario, default="")
    def __str__(self):
        return(f"{self.user.username}|{self.cedula} : {self.nombres} {self.apellidos}")
    

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    creado_en = models.DateField(auto_now_add=True)
    nombre_cliente = models.CharField(max_length=200)
    direccion = models.TextField(blank=True)
    correo = models.CharField(max_length=150, blank=True, null=True, default="")
    telefono = models.CharField(max_length=12, null=True)
    telefono2 = models.CharField(max_length=12, blank=True, null=True)
    rif = models.CharField(max_length=15)
    cliente_image = models.ImageField(blank=True, upload_to=generar_nombre_imgen_cliente, default="")
    
    @classmethod
    def get_default_pk(cls):
        cliente, created = cls.objects.get_or_create(
            nombre_cliente='NONE', 
            
        )
        return cliente.pk
    
    def __str__(self):
        return(f"{self.id_cliente} : {self.nombre_cliente}")

class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    creado_en = models.DateField(auto_now_add=True)
    nombre_proveedor = models.CharField(max_length=200)
    correo = models.CharField(max_length=150, blank=True)
    tlf_proveedor = models.CharField(max_length=12, blank = True, null=True)
    nota_proveedor = models.TextField(blank = True)
    def __str__(self):
        return(f"{self.id_proveedor} : {self.nombre_proveedor}")


class Almacen(models.Model):
    id_almacen = models.AutoField(primary_key=True)
    creado_en = models.DateField(auto_now_add=True)
    nombre_almacen = models.CharField(max_length=200)
    direccion = models.CharField(max_length=20, blank=True, null=True, default="")
    nota = models.TextField(max_length=20, blank=True, null=True, default="")
    def __str__(self):
        return(f"{self.id_almacen} - {self.nombre_almacen}")


class Destino(models.Model):
    id_destino = models.AutoField(primary_key=True)
    creado_en = models.DateField(auto_now_add=True)
    nombre_destino = models.CharField(max_length=200)
    ciudad = models.TextField()
    def __str__(self):
        return(f"{self.id_destino} : {self.ciudad} - {self.nombre_destino}")

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    creado_en = models.DateField(auto_now_add=True)
    cod_producto = models.CharField(max_length=20, blank=True)
    nombre_producto = models.CharField(max_length=200)
    descripcion_prod = models.TextField(blank=True)
    cant_min = models.PositiveIntegerField(default=0)  # Cambiado a PositiveIntegerField
    cant_max = models.PositiveIntegerField(default=0)  # Cambiado a PositiveIntegerField
    id_proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True)
    prod_image = models.ImageField(blank=True, upload_to=generar_nombre_imgen_producto, default="")
    def __str__(self):
        return(f"{self.cod_producto}-{self.nombre_producto}({self.cant_max};{self.cant_min})")

class Inventario(models.Model):
    id_inventario = models.AutoField(primary_key=True)
    creado_en = models.DateField(auto_now_add=True)
    precio_unit_ref = models.DecimalField(max_digits=9, decimal_places=3)
    cant_disponible = models.PositiveIntegerField(default=0)  # Cambiado a PositiveIntegerField
    cant_inicial = models.PositiveIntegerField(default=0)
    fecha_ult_mod_inv = models.DateField(default=timezone.now)  # Se establece la fecha por defecto
    producto = models.ForeignKey(Producto, on_delete=models.DO_NOTHING)
    nota = models.TextField(blank=True)
    id_almacen = models.ForeignKey(Almacen, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.id_inventario} : {self.producto.nombre_producto}- ({self.cant_disponible})"

class Registro_inventario(models.Model):
    id_registro = models.AutoField(primary_key=True)
    desc_accion = models.CharField(max_length=150)
    tipo_accion = models.CharField(max_length=150)
    fecha_accion = models.DateField(auto_now_add=True)
    cantidad_accion = models.PositiveIntegerField()
    id_inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE)

class Prod_Dest(models.Model):
    id_prod_dest = models.AutoField(primary_key=True)
    creado_en = models.DateField(auto_now_add=True)
    id_producto = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    id_destino = models.ForeignKey(Destino, on_delete=models.CASCADE)
    consumo_prom_dia = models.DecimalField(max_digits=9, decimal_places=2)
    fecha_ult_sumin = models.DateField()
    class Meta:
        unique_together = ('id_destino', 'id_producto')

class Orden(models.Model):
    id_orden = models.AutoField(primary_key=True)
    creado_en = models.DateField(auto_now_add=True)
    num_orden = models.IntegerField()
    fecha_emision = models.DateField(blank=True, null= True)
    estado = models.CharField(max_length=20)
    num_factura = models.CharField(max_length=20)
    desc_requisicion = models.CharField(max_length=20)
    fecha_requisicion = models.DateField(blank=True, null= True)
    fecha_entrega = models.DateField(blank=True, null= True)
    solicitado = models.CharField(max_length=25)
    tlf_solicitado = models.CharField(max_length=12, blank=True, null=True)
    fecha_ult_mod = models.DateField(auto_now_add=True)
    num_lote = models.CharField(max_length=20)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null = True, default=Cliente.get_default_pk)
    id_destino = models.ForeignKey(Destino, on_delete=models.SET_NULL, null = True)
    id_usuario = models.ForeignKey(User, on_delete=models.RESTRICT, null=True)
    
    @property
    def get_total_general(self):
        return sum(item.get_total for item in self.orden_producto_set.all())
    
    def __str__(self):
        return(f"id:{self.id_orden}-numOrden:{self.num_orden}-desc:{self.desc_requisicion}")

class Orden_Producto(models.Model):
    id_orden_prod = models.AutoField(primary_key=True)
    creado_en = models.DateField(auto_now_add=True)
    cantidad = models.IntegerField()
    precio_unit = models.DecimalField(max_digits=9, decimal_places=3, default=0.0)
    empaque = models.CharField(max_length=20)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True)
    id_orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
    
    @property
    def get_total(self):
        return self.cantidad * self.precio_unit
    