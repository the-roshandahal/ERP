# Generated by Django 4.1.4 on 2023-03-10 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_product_is_vatable'),
        ('finance', '0004_auto_20230308_1322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='product',
            field=models.ManyToManyField(to='products.product'),
        ),
    ]