# Generated by Django 4.0.6 on 2022-08-07 15:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0012_cart_total_price_alter_cart_quantity_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='total_Price',
        ),
    ]
