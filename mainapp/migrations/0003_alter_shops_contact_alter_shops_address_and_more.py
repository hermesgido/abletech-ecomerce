# Generated by Django 4.0.6 on 2022-08-04 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_remove_shop_categories_seller_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shops',
            name='Contact',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='shops',
            name='address',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='shops',
            name='latitude',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='shops',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='seller logo'),
        ),
        migrations.AlterField(
            model_name='shops',
            name='longitude',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='shops',
            name='registered_Date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='shops',
            name='shop_name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
