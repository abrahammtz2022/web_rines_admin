# Generated by Django 3.0.4 on 2023-05-19 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0013_cardex_prod_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardex',
            name='prod_user_store',
            field=models.IntegerField(default=0),
        ),
    ]
