# Generated by Django 4.0.6 on 2022-08-07 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0016_alter_product_brand_name_alter_product_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_attribute',
            name='value',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
