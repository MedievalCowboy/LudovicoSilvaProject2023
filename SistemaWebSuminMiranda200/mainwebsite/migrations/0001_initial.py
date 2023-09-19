# Generated by Django 4.2.5 on 2023-09-18 20:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Almacen',
            fields=[
                ('id_almacen', models.IntegerField(primary_key=True, serialize=False)),
                ('creado_en', models.DateField(auto_now_add=True)),
                ('nombre_almacen', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id_cliente', models.IntegerField(primary_key=True, serialize=False)),
                ('creado_en', models.DateField(auto_now_add=True)),
                ('nombre_cliente', models.CharField(max_length=200)),
                ('direccion', models.TextField()),
                ('telefono', models.CharField(max_length=12)),
                ('rif', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Destino',
            fields=[
                ('id_destino', models.IntegerField(primary_key=True, serialize=False)),
                ('creado_en', models.DateField(auto_now_add=True)),
                ('nombre_destino', models.CharField(max_length=200)),
                ('ciudad', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('id_producto', models.IntegerField(primary_key=True, serialize=False)),
                ('creado_en', models.DateField(auto_now_add=True)),
                ('nombre_producto', models.CharField(max_length=200)),
                ('descripcion_prod', models.TextField()),
                ('cod_producto', models.CharField(max_length=10)),
                ('precio_unit_ref', models.DecimalField(decimal_places=3, max_digits=9)),
                ('cant_disponible', models.IntegerField()),
                ('cant_min', models.IntegerField()),
                ('cant_max', models.IntegerField()),
                ('fecha_ult_mod_inv', models.DateField()),
                ('nota', models.TextField()),
                ('id_almacen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainwebsite.almacen')),
            ],
        ),
        migrations.CreateModel(
            name='Orden_prod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado_en', models.DateField(auto_now_add=True)),
                ('cantidad', models.IntegerField()),
                ('empaque', models.CharField(max_length=15)),
                ('id_inventario', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mainwebsite.inventario')),
            ],
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id_proveedor', models.IntegerField(primary_key=True, serialize=False)),
                ('creado_en', models.DateField(auto_now_add=True)),
                ('nombre_proveedor', models.CharField(max_length=200)),
                ('correo', models.CharField(max_length=150)),
                ('tlf_proveedor', models.CharField(max_length=12)),
                ('nota_proveedor', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Registro_inventario',
            fields=[
                ('id_registro', models.IntegerField(primary_key=True, serialize=False)),
                ('creado_en', models.DateField(auto_now_add=True)),
                ('desc_accion', models.CharField(max_length=150)),
                ('tipo_accion', models.CharField(max_length=150)),
                ('fecha_accion', models.DateField(auto_now_add=True)),
                ('cantidad', models.IntegerField()),
                ('id_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainwebsite.inventario')),
            ],
        ),
        migrations.CreateModel(
            name='Prod_Dest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado_en', models.DateField(auto_now_add=True)),
                ('consumo_prom_dia', models.DecimalField(decimal_places=3, max_digits=9)),
                ('fecha_ult_sumin', models.DateField()),
                ('id_destino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainwebsite.destino')),
                ('id_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainwebsite.inventario')),
            ],
        ),
        migrations.CreateModel(
            name='Ordenes',
            fields=[
                ('id_orden', models.IntegerField(primary_key=True, serialize=False)),
                ('creado_en', models.DateField(auto_now_add=True)),
                ('num_orden', models.IntegerField()),
                ('fecha_emision', models.DateField()),
                ('estado', models.CharField(max_length=20)),
                ('num_factura', models.CharField(max_length=40)),
                ('desc_requisicion', models.CharField(max_length=20)),
                ('fecha_requisicion', models.DateField()),
                ('fecha_entrega', models.DateField()),
                ('solicitado', models.CharField(max_length=25)),
                ('tlf_solicitado', models.CharField(max_length=12)),
                ('fecha_ult_mod', models.DateField()),
                ('num_lote', models.CharField(max_length=20)),
                ('id_cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainwebsite.cliente')),
                ('id_destino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainwebsite.destino')),
                ('id_producto', models.ManyToManyField(through='mainwebsite.Orden_prod', to='mainwebsite.inventario')),
            ],
        ),
        migrations.AddField(
            model_name='orden_prod',
            name='id_orden',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mainwebsite.ordenes'),
        ),
        migrations.AddField(
            model_name='inventario',
            name='id_destino',
            field=models.ManyToManyField(through='mainwebsite.Prod_Dest', to='mainwebsite.destino'),
        ),
        migrations.AddField(
            model_name='inventario',
            name='id_proveedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainwebsite.proveedor'),
        ),
    ]
