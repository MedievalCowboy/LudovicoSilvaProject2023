# Generated by Django 4.2.5 on 2023-10-19 02:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Almacen',
            fields=[
                ('id_almacen', models.AutoField(primary_key=True, serialize=False)),
                ('creado_en', models.DateField(auto_now_add=True)),
                ('nombre_almacen', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id_cliente', models.AutoField(primary_key=True, serialize=False)),
                ('creado_en', models.DateField(auto_now_add=True)),
                ('nombre_cliente', models.CharField(max_length=200)),
                ('direccion', models.TextField(blank=True)),
                ('telefono', models.CharField(blank=True, max_length=12)),
                ('rif', models.CharField(blank=True, max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Destino',
            fields=[
                ('id_destino', models.AutoField(primary_key=True, serialize=False)),
                ('creado_en', models.DateField(auto_now_add=True)),
                ('nombre_destino', models.CharField(max_length=200)),
                ('ciudad', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('id_inventario', models.AutoField(primary_key=True, serialize=False)),
                ('creado_en', models.DateField(auto_now_add=True)),
                ('precio_unit_ref', models.DecimalField(decimal_places=3, max_digits=9)),
                ('cant_disponible', models.IntegerField()),
                ('cant_min', models.IntegerField()),
                ('cant_max', models.IntegerField()),
                ('fecha_ult_mod_inv', models.DateField()),
                ('nota', models.TextField(blank=True)),
                ('id_almacen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainwebsite.almacen')),
            ],
        ),
        migrations.CreateModel(
            name='Orden',
            fields=[
                ('id_orden', models.AutoField(primary_key=True, serialize=False)),
                ('creado_en', models.DateField(auto_now_add=True)),
                ('num_orden', models.IntegerField()),
                ('fecha_emision', models.DateField(blank=True, null=True)),
                ('estado', models.CharField(max_length=20)),
                ('num_factura', models.CharField(max_length=40)),
                ('desc_requisicion', models.CharField(max_length=20)),
                ('fecha_requisicion', models.DateField(blank=True, null=True)),
                ('fecha_entrega', models.DateField(blank=True, null=True)),
                ('solicitado', models.CharField(max_length=25)),
                ('tlf_solicitado', models.CharField(blank=True, max_length=12)),
                ('fecha_ult_mod', models.DateField(auto_now_add=True)),
                ('num_lote', models.CharField(max_length=20)),
                ('id_cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainwebsite.cliente')),
                ('id_destino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainwebsite.destino')),
                ('id_usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id_proveedor', models.AutoField(primary_key=True, serialize=False)),
                ('creado_en', models.DateField(auto_now_add=True)),
                ('nombre_proveedor', models.CharField(max_length=200)),
                ('correo', models.CharField(blank=True, max_length=150)),
                ('tlf_proveedor', models.CharField(blank=True, max_length=12)),
                ('nota_proveedor', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Registro_inventario',
            fields=[
                ('id_registro', models.AutoField(primary_key=True, serialize=False)),
                ('creado_en', models.DateField(auto_now_add=True)),
                ('desc_accion', models.CharField(max_length=150)),
                ('tipo_accion', models.CharField(max_length=150)),
                ('fecha_accion', models.DateField(auto_now_add=True)),
                ('cantidad', models.IntegerField()),
                ('id_inventario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainwebsite.inventario')),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id_producto', models.AutoField(primary_key=True, serialize=False)),
                ('creado_en', models.DateField(auto_now_add=True)),
                ('cod_producto', models.CharField(blank=True, max_length=10)),
                ('nombre_producto', models.CharField(max_length=200)),
                ('descripcion_prod', models.TextField(blank=True)),
                ('id_proveedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainwebsite.proveedor')),
            ],
        ),
        migrations.CreateModel(
            name='Prod_Dest',
            fields=[
                ('id_prod_dest', models.AutoField(primary_key=True, serialize=False)),
                ('creado_en', models.DateField(auto_now_add=True)),
                ('consumo_prom_dia', models.DecimalField(decimal_places=3, max_digits=9)),
                ('fecha_ult_sumin', models.DateField()),
                ('id_destino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainwebsite.destino')),
                ('id_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainwebsite.inventario')),
            ],
        ),
        migrations.CreateModel(
            name='Orden_Producto',
            fields=[
                ('id_orden_prod', models.AutoField(primary_key=True, serialize=False)),
                ('creado_en', models.DateField(auto_now_add=True)),
                ('cantidad', models.IntegerField()),
                ('precio_unit', models.DecimalField(decimal_places=3, default=0.0, max_digits=9)),
                ('empaque', models.CharField(max_length=20)),
                ('id_orden', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainwebsite.orden')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainwebsite.producto')),
            ],
        ),
        migrations.AddField(
            model_name='inventario',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainwebsite.producto'),
        ),
    ]
