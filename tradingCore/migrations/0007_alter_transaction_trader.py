# Generated by Django 4.1.7 on 2023-03-20 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tradingCore', '0006_delete_futures'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='trader',
            field=models.ForeignKey(on_delete=models.SET(None), to='tradingCore.trader'),
        ),
    ]
