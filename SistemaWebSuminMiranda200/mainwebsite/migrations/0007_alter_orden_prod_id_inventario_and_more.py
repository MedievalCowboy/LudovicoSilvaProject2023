# Generated by Django 4.2.5 on 2023-10-11 17:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainwebsite', '0006_alter_orden_fecha_entrega_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orden_prod',
            name='id_inventario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainwebsite.inventario'),
        ),
        migrations.AlterField(
            model_name='orden_prod',
            name='id_orden',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainwebsite.orden'),
        ),
    ]
