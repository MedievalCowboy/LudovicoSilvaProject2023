# Generated by Django 4.2.5 on 2023-10-11 17:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainwebsite', '0007_alter_orden_prod_id_inventario_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Orden_prod',
            new_name='Orden_Producto',
        ),
        migrations.RenameField(
            model_name='orden_producto',
            old_name='id_inventario',
            new_name='producto',
        ),
        migrations.RemoveField(
            model_name='orden',
            name='id_producto',
        ),
    ]