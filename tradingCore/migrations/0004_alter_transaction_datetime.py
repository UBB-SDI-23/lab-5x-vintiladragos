# Generated by Django 4.1.7 on 2023-03-13 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tradingCore', '0003_futures_trader_remove_stock_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='datetime',
            field=models.DateTimeField(auto_now=True),
        ),
    ]