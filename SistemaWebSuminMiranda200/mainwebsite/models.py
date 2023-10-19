from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone





class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    creado_en = models.DateField(auto_now_add=True)
    nombre_cliente = models.CharField(max_length=200)
    direccion = models.TextField(blank=True)
    telefono = models.CharField(max_length=12, blank=True)
    rif = models.CharField(max_length=15, blank=True)
    def __str__(self):
        return(f"{self.id_cliente} : {self.nombre_cliente}")

class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    creado_en = models.DateField(auto_now_add=True)
    nombre_proveedor = models.CharField(max_length=200)
    correo = models.CharField(max_length=150, blank=True)
    tlf_proveedor = models.CharField(max_length=12, blank = True)
    nota_proveedor = models.TextField(blank = True)
    def __str__(self):
        return(f"{self.id_proveedor} : {self.nombre_proveedor}")


class Almacen(models.Model):
    id_almacen = models.AutoField(primary_key=True)
    creado_en = models.DateField(auto_now_add=True)
    nombre_almacen = models.CharField(max_length=200)
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
    cod_producto = models.CharField(max_length=10, blank=True)
    nombre_producto = models.CharField(max_length=200)
    descripcion_prod = models.TextField(blank=True)
    cant_min = models.PositiveIntegerField(default=0)  # Cambiado a PositiveIntegerField
    cant_max = models.PositiveIntegerField(default=0)  # Cambiado a PositiveIntegerField
    id_proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True)
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
    consumo_prom_dia = models.DecimalField(max_digits=9, decimal_places=3)
    fecha_ult_sumin = models.DateField()

class Orden(models.Model):
    id_orden = models.AutoField(primary_key=True)
    creado_en = models.DateField(auto_now_add=True)
    num_orden = models.IntegerField()
    fecha_emision = models.DateField(blank=True, null= True)
    estado = models.CharField(max_length=20)
    num_factura = models.CharField(max_length=40)
    desc_requisicion = models.CharField(max_length=20)
    fecha_requisicion = models.DateField(blank=True, null= True)
    fecha_entrega = models.DateField(blank=True, null= True)
    solicitado = models.CharField(max_length=25)
    tlf_solicitado = models.CharField(max_length=12, blank=True)
    fecha_ult_mod = models.DateField(auto_now_add=True)
    num_lote = models.CharField(max_length=20)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null = True)
    id_destino = models.ForeignKey(Destino, on_delete=models.SET_NULL, null = True)
    id_usuario = models.ForeignKey(User, on_delete=models.RESTRICT, null=True)
    def __str__(self):
        return(f"id:{self.id_orden}-numOrden:{self.num_orden}-desc:{self.desc_requisicion}")

class Orden_Producto(models.Model):
    id_orden_prod = models.AutoField(primary_key=True)
    creado_en = models.DateField(auto_now_add=True)
    cantidad = models.IntegerField()
    precio_unit = models.DecimalField(max_digits=9, decimal_places=3, default=0.0)
    empaque = models.CharField(max_length=20)
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    id_orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
    # Relaciones