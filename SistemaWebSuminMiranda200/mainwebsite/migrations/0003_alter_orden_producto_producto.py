# Generated by Django 4.2.5 on 2023-10-19 02:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainwebsite', '0002_alter_producto_id_proveedor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orden_producto',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mainwebsite.producto'),
        ),
    ]
