# Generated by Django 4.0.6 on 2022-08-07 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0011_remove_cart_product_id_cart_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='total_Price',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='cart',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='cart',
            name='unit_Price',
            field=models.IntegerField(default=0),
        ),
    ]
