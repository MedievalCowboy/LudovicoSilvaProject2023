# Generated by Django 4.2.5 on 2023-10-21 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainwebsite', '0013_alter_inventario_cant_disponible'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='telefono',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='orden',
            name='tlf_solicitado',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='tlf_proveedor',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]