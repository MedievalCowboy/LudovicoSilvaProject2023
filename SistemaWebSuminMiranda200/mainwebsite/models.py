from django.db import models
from django.contrib.auth.models import User


class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    creado_en = models.DateField(auto_now_add=True)
    nombre_cliente = models.CharField(max_length=200)
    direccion = models.TextField(blank=True)
    telefono = models.CharField(max_length=12, blank=True)
    rif = models.CharField(max_length=15, blank=True)

class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    creado_en = models.DateField(auto_now_add=True)
    nombre_proveedor = models.CharField(max_length=200)
    correo = models.CharField(max_length=150, blank=True)
    tlf_proveedor = models.CharField(max_length=12, blank = True)
    nota_proveedor = models.TextField(blank = True)


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


class Inventario(models.Model):
    id_producto = models.AutoField(primary_key=True)
    creado_en = models.DateField(auto_now_add=True)
    nombre_producto = models.CharField(max_length=200)
    descripcion_prod = models.TextField(blank=True)
    cod_producto = models.CharField(max_length=10, blank=True)
    precio_unit_ref = models.DecimalField(max_digits=9, decimal_places=3)
    cant_disponible = models.IntegerField()
    cant_min = models.IntegerField()
    cant_max = models.IntegerField()
    fecha_ult_mod_inv = models.DateField()
    nota = models.TextField(blank= True)
    id_destino = models.ManyToManyField(Destino, through='Prod_Dest')
    id_proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    id_almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE)


class Registro_inventario(models.Model):
    id_registro = models.AutoField(primary_key=True)
    creado_en = models.DateField(auto_now_add=True)
    desc_accion = models.CharField(max_length=150)
    tipo_accion = models.CharField(max_length=150)
    fecha_accion = models.DateField(auto_now_add=True)
    cantidad = models.IntegerField()
    id_producto = models.ForeignKey(Inventario, on_delete=models.CASCADE)

class Prod_Dest(models.Model):
    creado_en = models.DateField(auto_now_add=True)
    id_producto = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    id_destino = models.ForeignKey(Destino, on_delete=models.CASCADE)
    consumo_prom_dia = models.DecimalField(max_digits=9, decimal_places=3)
    fecha_ult_sumin = models.DateField()

class Orden(models.Model):
    id_orden = models.AutoField(primary_key=True)
    creado_en = models.DateField(auto_now_add=True)
    num_orden = models.IntegerField()
    fecha_emision = models.DateField()
    estado = models.CharField(max_length=20)
    num_factura = models.CharField(max_length=40)
    desc_requisicion = models.CharField(max_length=20)
    fecha_requisicion = models.DateField()
    fecha_entrega = models.DateField()
    solicitado = models.CharField(max_length=25)
    tlf_solicitado = models.CharField(max_length=12)
    fecha_ult_mod = models.DateField()
    num_lote = models.CharField(max_length=20)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    id_producto = models.ManyToManyField(Inventario, through='Orden_prod')
    id_destino = models.ForeignKey(Destino, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(User, on_delete=models.RESTRICT, null=True)
    def __str__(self):
        return(f"id:{self.id_orden}-numOrden:{self.num_orden}-desc:{self.desc_requisicion}")

class Orden_Prod(models.Model):
    creado_en = models.DateField(auto_now_add=True)
    cantidad = models.IntegerField()
    precio_unit = models.DecimalField
    empaque = models.CharField(max_length=15)
    id_inventario = models.ForeignKey(Inventario,on_delete=models.DO_NOTHING)
    id_orden = models.ForeignKey(Orden, on_delete=models.DO_NOTHING)
    # Relaciones