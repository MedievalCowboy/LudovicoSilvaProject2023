# Generated by Django 5.0.1 on 2025-01-04 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainwebsite', '0021_alter_producto_prod_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='correo',
            field=models.CharField(blank=True, default='', max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='telefono2',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]
