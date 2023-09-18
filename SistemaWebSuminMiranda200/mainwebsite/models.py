from django.db import models



# Create your models here.
class Cliente(models.Model):
    id_cliente = models.IntegerField(primary_key=True)
    nombre_cliente = models.CharField(max_length=200)
    direccion = models.TextField()
    telefono = models.CharField(max_length=12)
    rif = models.CharField(max_length=15)

class Orden_prod(models.Model):
    cantidad = models.IntegerField()
    precio_unit = models.DecimalField
    empaque = models.CharField(max_length=15)
    #Relaciones
  

class Proveedor(models.Model):
    id_proveedor = models.IntegerField(primary_key=True)
    nombre_proveedor = models.CharField(max_length=200)
    correo = models.CharField(max_length=150)
    tlf_proveedor = models.CharField(max_length=12)
    nota_proveedor = models.TextField()

class Almacen(models.Model):
    id_almacen = models.IntegerField(primary_key=True)
    nombre_almacen = models.CharField(max_length=200)

class Destino(models.Model):
    id_destino = models.IntegerField(primary_key=True)
    nombre_destino = models.CharField(max_length=200)
    ciudad = models.TextField()

class Inventario(models.Model):
   id_producto = models.IntegerField(primary_key=True)
   nombre_producto = models.CharField(max_length=200)
   descripcion_prod = models.TextField()
   cod_producto = models.CharField(max_length=10)
   precio_unit_ref = models.DecimalField(max_digits=9, decimal_places=3)
   cant_disponible = models.IntegerField()
   cant_min = models.IntegerField()
   cant_max = models.IntegerField()
   fecha_ult_mod_inv = models.DateField()
   nota = models.TextField()
   id_destino = models.ManyToManyField(Destino, through='Prod_Dest')
   id_proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
   id_almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE)

class Registro_inventario(models.Model):
    id_registro = models.IntegerField(primary_key=True)
    desc_accion = models.CharField(max_length=150)
    tipo_accion = models.CharField(max_length=150)
    fecha_accion = models.DateField()
    cantidad = models.IntegerField()
    id_producto = models.ForeignKey(Inventario, on_delete=models.CASCADE)

class Prod_Dest(models.Model):
    id_producto = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    id_destino = models.ForeignKey(Destino, on_delete=models.CASCADE)
    consumo_prom_dia = models.IntegerField()
    fecha_ult_sumin = models.DateField()

class Ordenes(models.Model):
     id_orden = models.IntegerField(primary_key=True)
     num_orden = models.IntegerField()
     fecha_emision = models.DateField()
     estado = models.CharField(max_length=20)
     num_factura = models.IntegerField()
     desc_requisicion = models.CharField(max_length=20)
     fecha_requisicion = models.DateField()
     fecha_entrega = models.DateField()
     solicitado = models.CharField(max_length=25)
     tlf_solicitado = models.CharField(max_length=12)
     fecha_ult_mod = models.DateField()
     num_lote = models.CharField(max_length=20)
     id_cliente = models.ForeignKey(Cliente, on_delete= models.CASCADE)
     id_producto = models.ManyToManyField(Inventario, through='Orden_prod')
     id_destino = models.ForeignKey(Destino, on_delete=models.CASCADE)
