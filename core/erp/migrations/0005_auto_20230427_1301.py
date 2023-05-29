# Generated by Django 3.0.4 on 2023-04-27 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0004_alter_client_names'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sucursal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField(default=0, unique=True, verbose_name='Numero Sucursal')),
                ('nombre', models.CharField(max_length=80, verbose_name='Nombre Sucursal')),
            ],
            options={
                'verbose_name': 'Sucursal',
                'verbose_name_plural': 'Sucursales',
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='product',
            name='nexistencia',
            field=models.IntegerField(default=0, verbose_name='Existencia'),
        ),
        migrations.AddField(
            model_name='product',
            name='noSucursal',
            field=models.IntegerField(default=0, verbose_name='No. de Sucursal'),
        ),
        migrations.AddField(
            model_name='product',
            name='pcosto',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9, verbose_name='Costo de Venta'),
        ),
        migrations.AddField(
            model_name='product',
            name='umedida',
            field=models.CharField(default='pieza', max_length=20, verbose_name='Unidad de Medida'),
        ),
        migrations.AlterField(
            model_name='client',
            name='dni',
            field=models.CharField(max_length=13, unique=True, verbose_name='RFC'),
        ),
    ]
